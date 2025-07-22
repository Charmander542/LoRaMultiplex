
import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):
    """
    Gated Router Block:
    - Passes data for channels that cross a power threshold.
    - Includes a message port to output the set of active channels on change.
    - Keeps channels open for a configurable duration after power drops.
    
    Compatible with GNU Radio 3.8
    """
    def __init__(self, num_channels=10, threshold_db=-40.0, hold_time_s=2.0, samp_rate=1e6):
        # The input signature is num_channels complex streams followed by one float vector stream
        in_sigs = [np.complex64] * num_channels
        in_sigs.append((np.float32, num_channels))
        
        # The output signature is num_channels complex streams
        out_sigs = [np.complex64] * num_channels

        gr.sync_block.__init__(
            self,
            name="Gated Router (GR3.8)",
            in_sig=in_sigs,
            out_sig=out_sigs,
        )

        self.num_channels = num_channels
        self.samp_rate = samp_rate
        self.threshold = 10**(threshold_db / 10.0)
        
        # Calculate the number of samples to hold the channel open
        self.hold_samples = int(hold_time_s * self.samp_rate)

        # State to track which channels are currently active
        self.active_channels = [False] * self.num_channels
        # State to remember the previous state for change detection
        self.last_active_state = list(self.active_channels)
        # Hold counters for each channel
        self.hold_counters = [0] * self.num_channels

        # Register the message port for debugging active channels
        self.message_port_register_out(pmt.intern("active_channels_debug"))

    def work(self, input_items, output_items):
        # The last input is the buffer containing power vectors
        power_vector_buffer = input_items[self.num_channels]
        
        # Number of items to process, determined by the scheduler
        num_to_process = len(output_items[0])

        if len(power_vector_buffer) > 0:
            # Use the first available power vector for this work call
            power_vector = power_vector_buffer[0]
            for i in range(self.num_channels):
                # If power is above threshold, activate channel and reset hold counter
                if power_vector[i] > self.threshold:
                    self.active_channels[i] = True
                    self.hold_counters[i] = self.hold_samples
                # If channel is in hold state, keep it active and decrement counter
                elif self.hold_counters[i] > 0:
                    self.active_channels[i] = True
                    self.hold_counters[i] -= num_to_process
                    if self.hold_counters[i] < 0:
                        self.hold_counters[i] = 0
                # Otherwise, the channel is inactive
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

        # If the set of active channels has changed, send a debug message
        if self.active_channels != self.last_active_state:
            active_indices = [i for i, status in enumerate(self.active_channels) if status]
            
            # --- MODIFICATION FOR GR 3.8 ---
            # Replaced f-string with .format() for Python 2/3.5 compatibility
            debug_str = "Active: {}".format(active_indices)
            
            msg = pmt.to_pmt(debug_str)
            self.message_port_pub(pmt.intern("active_channels_debug"), msg)
            self.last_active_state = list(self.active_channels)

        # Gate the output streams
        for i in range(self.num_channels):
            if self.active_channels[i]:
                # Pass data through for active channels
                output_items[i][:num_to_process] = input_items[i][:num_to_process]
            else:
                # Output zeros for inactive channels
                output_items[i][:num_to_process] = 0

        # Return the number of items produced on each output stream
        return num_to_process

      