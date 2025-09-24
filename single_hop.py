#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Hopping (by re-tuning the USRP)
# Generated: Thu Jul 24 17:26:10 2025
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio import uhd
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import lora
import osmosdr
import wx


class single(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Hopping")

        ##################################################
        # Variables
        ##################################################
        self.sf = sf = 7
        self.samp_rate = samp_rate = 1e6
        self.bw = bw = 125000
        self.target_freq = target_freq = [902.3e6]#, 902.5e6, 902.7e6, 902.9e6, 903.1e6, 903.3e6, 903.5e6, 903.7e6, 903.9e6, 904.1e6]
        self.hop_interval = hop_interval = 1000 # 1 second hop interval
        self.freq_index = freq_index = 0
        
        # This now represents the INITIAL frequency. It will be updated by the timer.
        self.capture_freq = capture_freq = self.target_freq[self.freq_index]

        # Other variables
        self.downlink = downlink = False
        self.decimation = decimation = 1

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_c(
            self.GetWin(),
            baseband_freq=capture_freq, # Will be updated
            sample_rate=samp_rate
        )
        self.Add(self.wxgui_fftsink2_1.win)

        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("serial=3134B8C", "")),
            uhd.stream_args(cpu_format="fc32", channels=range(1))
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(capture_freq, 0) # Will be updated
        self.uhd_usrp_source_0.set_gain(20, 0)
        
        self.lora_message_socket_sink_0 = lora.message_socket_sink('127.0.0.1', 40868, 0)

        # The LoRa receiver is now configured to listen AT the USRP's center frequency.
        # Its internal frequency parameter is now what defines this relationship.
        self.lora_lora_receiver_0 = lora.lora_receiver(
            samp_rate, capture_freq, ([capture_freq]), bw, sf, 
            False, 4, True, False, downlink, decimation, False, False
        )
        
        ##################################################
        # Timer for frequency hopping
        ##################################################
        self.hop_timer = wx.Timer(self.GetWin(), wx.ID_ANY)
        self.GetWin().Bind(wx.EVT_TIMER, self.perform_hop, self.hop_timer)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.lora_lora_receiver_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_1, 0))
        self.msg_connect((self.lora_lora_receiver_0, 'frames'), (self.lora_message_socket_sink_0, 'in'))

    def perform_hop(self, event):
        """The main hopping logic by re-tuning the USRP."""
        self.freq_index = (self.freq_index + 1) % len(self.target_freq)
        new_freq = self.target_freq[self.freq_index]

        # Command the USRP hardware to retune to the new frequency
        self.uhd_usrp_source_0.set_center_freq(new_freq, 0)

        # Update the FFT plot to reflect the new center frequency
        self.wxgui_fftsink2_1.set_baseband_freq(new_freq)
        
        print("Hopped USRP to: %.2f MHz" % (new_freq / 1e6))

    def Start(self, *args, **kwargs):
        super(single, self).Start(*args, **kwargs)
        if hasattr(self, 'hop_interval') and self.hop_interval > 0:
            print("Starting on frequency: %.2f MHz" % (self.capture_freq / 1e6))
            self.hop_timer.Start(self.hop_interval)

    def Stop(self, *args, **kwargs):
        if hasattr(self, 'hop_timer'):
            self.hop_timer.Stop()
        super(single, self).Stop(*args, **kwargs)

    # --- Other Getter/Setter Methods ---
    def get_sf(self): return self.sf
    def get_samp_rate(self): return self.samp_rate
    def get_bw(self): return self.bw
    def get_target_freq(self): return self.target_freq
    def get_capture_freq(self): 
        # Return the current frequency of the USRP
        return self.uhd_usrp_source_0.get_center_freq()

def main(top_block_cls=single, options=None):
    try:
        tb = top_block_cls()
        tb.Start(True)
        tb.Wait()
    except Exception as e:
        print "Error starting flowgraph: %s" % e
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
