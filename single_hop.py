#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Final Working LoRa Frequency Hopper
##################################################

# --- Standard Python Imports ---
import sys
import traceback
import ctypes

# --- GNU Radio and WX Imports ---
from gnuradio import gr
from gnuradio import eng_notation
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio import filter # Import the full filter module
from gnuradio.wxgui import fftsink2
from grc_gnuradio import wxgui as grc_wxgui
import wx
import lora

# --- X11 Threading Support (Standard GRC Boilerplate) ---
if __name__ == '__main__':
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

        #####################################################################
        # STEP 1: DEFINE VARIABLES AND TIMER *BEFORE* PARENT INITIALIZATION
        # This is critical to prevent the __init__ race condition.
        #####################################################################

        # --- Hopping Configuration ---
        self.target_freq_list = [
            902.3e6, 902.5e6, 902.7e6, 902.9e6, 903.1e6, 903.3e6,
            903.5e6, 903.7e6, 903.9e6, 904.1e6
        ]
        self.hop_interval_ms = 1000  # Time to wait on each frequency
        self.current_freq_index = 0

        # --- Create the Hopping Timer Object ---
        # The parent __init__ will call Start, which needs this timer to exist.
        self.hop_timer = wx.Timer(self, wx.ID_ANY)
        

        #####################################################################
        # STEP 2: INITIALIZE THE PARENT WX GUI CLASS
        # Now that the timer exists, this call is safe.
        #####################################################################
        grc_wxgui.top_block_gui.__init__(self, title="Final Working LoRa Hopper")
        # From this point on, the GUI is ready.
        
        # Bind the timer event *after* the parent is initialized
        self.Bind(wx.EVT_TIMER, self._handle_hop_timer, self.hop_timer)


        #####################################################################
        # STEP 3: DEFINE REMAINING VARIABLES AND CREATE BLOCKS
        #####################################################################

        # --- Basic LoRa Parameters ---
        self.sf = sf = 7
        self.bw = bw = 125000

        # --- SDR and Sampling Parameters ---
        self.samp_rate = samp_rate = 1e6
        self.capture_freq = capture_freq = 903e6
        self.sdr_gain = sdr_gain = 30

        # --- Resampling Parameters ---
        interp = 5
        decim = 8
        self.resampled_rate = samp_rate * interp / decim

        # --- Create Blocks ---
        self.uhd_source = uhd.usrp_source(
            device_addr="serial=3134B8C",
            stream_args=uhd.stream_args(cpu_format="fc32", channels=range(1)),
        )
        self.resampler = filter.rational_resampler_ccc(interp, decim, None, None)
        self.lora_receiver = lora.lora_receiver(
            self.resampled_rate, capture_freq, [self.target_freq_list[0]],
            bw, sf, crc=True, implicit=False
        )
        self.fft_sink = fftsink2.fft_sink_c(
            self.GetWin(), baseband_freq=capture_freq, sample_rate=samp_rate,
            fft_size=1024, title='FFT Plot'
        )
        self.Add(self.fft_sink.win)
        self.socket_sink = lora.message_socket_sink('127.0.0.1', 40868, 0)
        
        ##################################################
        # Set Block Parameters
        ##################################################
        self.uhd_source.set_samp_rate(samp_rate)
        self.uhd_source.set_center_freq(capture_freq, 0)
        self.uhd_source.set_gain(sdr_gain, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_source, 0), (self.resampler, 0))
        self.connect((self.resampler, 0), (self.lora_receiver, 0))
        self.connect((self.uhd_source, 0), (self.fft_sink, 0))
        self.msg_connect((self.lora_receiver, 'frames'), (self.socket_sink, 'in'))

    def Start(self, *args, **kwargs):
        """Overrides the default Start method to also start our hopping timer."""
        super(HoppingReceiver, self).Start(*args, **kwargs)
        if self.hop_interval_ms > 0:
            print("INFO: Starting frequency hopping timer with interval: %dms" % self.hop_interval_ms)
            self.hop_timer.Start(self.hop_interval_ms)

    def _handle_hop_timer(self, event):
        """This function is called every time the hop_timer fires."""
        self.current_freq_index = (self.current_freq_index + 1) % len(self.target_freq_list)
        new_freq = self.target_freq_list[self.current_freq_index]
        self.lora_receiver.set_frequencies([new_freq])
        print("Hopping to: %.3f MHz" % (new_freq / 1e6))


def main(top_block_cls=HoppingReceiver, options=None):
    """Main function to create and run the flowgraph with robust error handling."""
    try:
        tb = top_block_cls()
        tb.Start(True)
        tb.Wait()
    except Exception as e:
        print("\nFATAL: An error occurred while starting the flowgraph.")
        print("------------------------------------------------------")
        traceback.print_exc()
        print("------------------------------------------------------")


if __name__ == '__main__':
    main()
