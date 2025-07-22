import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):
    """
    Gated Router Block:
    - Passes data for channels that cross a power threshold.
    - Includes a message port to output the set of active channels on change.
    - Keeps channels open for a configurable duration after power drops.
    """
    def __init__(self, num_channels=40, threshold_db=-40.0, hold_time_s=2.0, samp_rate=1e6):
        self.threshold = 10**(threshold_db/10.0)
        self.num_channels = num_channels
        self.samp_rate = samp_rate
        # Calculate the number of samples to hold the channel open
        self.hold_samples = int(hold_time_s * self.samp_rate)

        in_sigs = [np.complex64] * self.num_channels
        in_sigs.append((np.float32, self.num_channels))
        out_sigs = [np.complex64] * self.num_channels

        gr.sync_block.__init__(
            self,
            name="Gated Router",
            in_sig=in_sigs,
            out_sig=out_sigs,
        )
        # State to track which channels are currently active
        self.active_channels = [False] * self.num_channels
        # State to remember the previous state for change detection
        self.last_active_state = list(self.active_channels)
        # Hold counters for each channel
        self.hold_counters = [0] * self.num_channels

        # Register the new message port for debugging
        self.message_port_register_out(pmt.intern("active_channels_debug"))

    def work(self, input_items, output_items):
        power_vector_buffer = input_items[self.num_channels]
        num_to_process = len(output_items[0])

        if len(power_vector_buffer) > 0:
            power_vector = power_vector_buffer[0]
            for i in range(self.num_channels):
                if power_vector[i] > self.threshold:
                    self.active_channels[i] = True
                    self.hold_counters[i] = self.hold_samples
                elif self.hold_counters[i] > 0:
                    self.active_channels[i] = True
                    self.hold_counters[i] -= num_to_process
                    if self.hold_counters[i] < 0:
                        self.hold_counters[i] = 0
                else:
                    self.active_channels[i] = False
        else:
            # If there's no new power vector, maintain the state based on hold counters
            for i in range(self.num_channels):
                if self.hold_counters[i] > 0:
                    self.active_channels[i] = True
                    self.hold_counters[i] -= num_to_process
                    if self.hold_counters[i] < 0:
                        self.hold_counters[i] = 0
                else:
                    self.active_channels[i] = False

        # Check if the state of active channels has changed
        if self.active_channels != self.last_active_state:
            active_indices = [i for i, status in enumerate(self.active_channels) if status]
            debug_str = f"Active: {active_indices}"
            msg = pmt.to_pmt(debug_str)
            self.message_port_pub(pmt.intern("active_channels_debug"), msg)
            self.last_active_state = list(self.active_channels)

        for i in range(self.num_channels):
            if self.active_channels[i]:
                output_items[i][:num_to_process] = input_items[i][:num_to_process]
            else:
                output_items[i][:num_to_process] = 0

        # In a sync_block, we return the number of items produced on each output stream.
        # The scheduler handles consuming the corresponding number of input items.
        # The explicit consume calls from the original code were incorrect for a sync_block.
        return num_to_process
