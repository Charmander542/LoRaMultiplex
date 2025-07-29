#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Functional LoRa Frequency Hopper
##################################################

# --- Standard Python Imports ---
import sys
import traceback

# --- GNU Radio Imports ---
from gnuradio import gr
from gnuradio import eng_notation
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio import filter # Import the full filter module for the resampler
from gnuradio.wxgui import fftsink2
from grc_gnuradio import wxgui as grc_wxgui

# --- WX GUI and Lora Imports ---
import wx
import lora

# --- X11 Threading Support (Standard GRC Boilerplate) ---
if __name__ == '__main__':
    import ctypes
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"


class HoppingReceiver(grc_wxgui.top_block_gui):
    """
    A GNU Radio flowgraph that receives LoRa signals, hopping between a
    predefined list of frequencies at a regular interval.
    """
    def __init__(self):
        # Initialize the parent WX GUI class
        grc_wxgui.top_block_gui.__init__(self, title="Functional LoRa Hopper")

        ##################################################
        # Variables
        ##################################################

        # --- Basic LoRa Parameters ---
        self.sf = sf = 7
        self.bw = bw = 125000

        # --- SDR and Sampling Parameters ---
        self.samp_rate = samp_rate = 1e6
        self.capture_freq = capture_freq = 903e6 # The center frequency for the SDR
        self.sdr_gain = sdr_gain = 30

        # --- Hopping Configuration ---
        self.target_freq_list = [
            902.3e6, 902.5e6, 902.7e6, 902.9e6, 903.1e6, 903.3e6,
            903.5e6, 903.7e6, 903.9e6, 904.1e6
        ]
        self.hop_interval_ms = 1000  # Time to wait on each frequency, in milliseconds
        self.current_freq_index = 0

        # --- Resampling Parameters ---
        interp = 5
        decim = 8
        self.resampled_rate = samp_rate * interp / decim # Calculate the new rate: 625 kHz

        ##################################################
        # Blocks
        ##################################################

        # 1. SDR Source (UHD for USRP)
        self.uhd_source = uhd.usrp_source(
            device_addr="serial=3134B8C",
            stream_args=uhd.stream_args(cpu_format="fc32", channels=range(1)),
        )
        self.uhd_source.set_samp_rate(samp_rate)
        self.uhd_source.set_center_freq(capture_freq, 0)
        self.uhd_source.set_gain(sdr_gain, 0)

        # 2. Rational Resampler (to reduce sample rate)
        self.resampler = filter.rational_resampler_ccc(
            interpolation=interp,
            decimation=decim,
            taps=None,  # Let GNU Radio generate a default low-pass filter
            fractional_bw=None,
        )

        # 3. LoRa Receiver
        # It is initialized with the RESAMPLED rate and the FIRST frequency in our list.
        self.lora_receiver = lora.lora_receiver(
            self.resampled_rate,
            capture_freq,
            [self.target_freq_list[self.current_freq_index]], # Note: must be a list
            bw, sf,
            crc=True, implicit=False,
        )

        # 4. GUI FFT Sink (to visualize the spectrum)
        # This connects to the high-rate source to see the full captured bandwidth.
        self.fft_sink = fftsink2.fft_sink_c(
            self.GetWin(),
            baseband_freq=capture_freq,
            y_per_div=10,
            y_divs=10,
            ref_level=0,
            sample_rate=samp_rate,
            fft_size=1024,
            title='FFT Plot (Full Capture)',
        )
        self.Add(self.fft_sink.win)

        # 5. Socket Sink (to output received LoRa messages)
        self.socket_sink = lora.message_socket_sink('127.0.0.1', 40868, 0)

        ##################################################
        # Frequency Hopping Timer
        ##################################################

        # A WX Timer that will call our hopping function periodically.
        self.hop_timer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self._handle_hop_timer, self.hop_timer)

        ##################################################
        # Connections
        ##################################################

        # Data Path:
        # UHD Source -> Resampler -> LoRa Receiver
        self.connect((self.uhd_source, 0), (self.resampler, 0))
        self.connect((self.resampler, 0), (self.lora_receiver, 0))
        
        # Visualization Path:
        # UHD Source -> FFT Sink
        self.connect((self.uhd_source, 0), (self.fft_sink, 0))

        # Message Path:
        # LoRa Receiver -> Socket Sink
        self.msg_connect((self.lora_receiver, 'frames'), (self.socket_sink, 'in'))

    def Start(self, *args, **kwargs):
        """Overrides the default Start method to also start our hopping timer."""
        super(HoppingReceiver, self).Start(*args, **kwargs)
        if self.hop_interval_ms > 0:
            self.hop_timer.Start(self.hop_interval_ms)

    def _handle_hop_timer(self, event):
        """This function is called every time the hop_timer fires."""
        # 1. Calculate the next frequency index, wrapping around the list.
        self.current_freq_index = (self.current_freq_index + 1) % len(self.target_freq_list)
        
        # 2. Get the new frequency from our list.
        new_freq = self.target_freq_list[self.current_freq_index]
        
        # 3. Command the LoRa receiver to retune to the new frequency.
        self.lora_receiver.set_frequencies([new_freq])
        
        # 4. Print to the console so we can see it working.
        print("Hopping to: %.3f MHz" % (new_freq / 1e6))


def main(top_block_cls=HoppingReceiver, options=None):
    """
    Main function to create and run the flowgraph.
    Includes robust error handling to catch crashes during initialization.
    """
    try:
        tb = top_block_cls()
        tb.Start(True)
        tb.Wait()
    except Exception as e:
        # This will catch any error during tb = top_block_cls()
        # and print the TRUE error message, not the misleading one.
        print("\nFATAL: An error occurred while starting the flowgraph.")
        print("------------------------------------------------------")
        traceback.print_exc()
        print("------------------------------------------------------")


if __name__ == '__main__':
    main()
