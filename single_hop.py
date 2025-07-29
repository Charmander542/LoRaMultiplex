#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Hopping (Final Corrected Version)
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
        # STEP 1: Call the parent constructor. This will internally call our
        # overridden Start() method below, but that's okay because of Step 4.
        grc_wxgui.top_block_gui.__init__(self, title="Hopping")

        ##################################################
        # STEP 2: Define all class variables.
        # These are now set on the object *after* the parent __init__ is done.
        ##################################################
        self.sf = sf = 7
        self.samp_rate = samp_rate = 1e6
        self.bw = bw = 125000
        self.target_freq = target_freq = [902.3e6, 902.5e6, 902.7e6, 902.9e6, 903.1e6, 903.3e6, 903.5e6, 903.7e6, 903.9e6, 904.1e6]
        self.hop_interval = hop_interval = 1000 # 1 second
        self.freq_index = freq_index = 0
        self.capture_freq = capture_freq = 903e6
        # (Other variables would go here)

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=self.capture_freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=self.samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_1.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("serial=3134B8C", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.capture_freq, 0)
        self.uhd_usrp_source_0.set_gain(20, 0)

        self.lora_message_socket_sink_0 = lora.message_socket_sink('127.0.0.1', 40868, 0)
        self.lora_lora_receiver_0 = lora.lora_receiver(self.samp_rate, self.capture_freq, ([self.target_freq[self.freq_index]]), self.bw, self.sf, False, 4, True, False, False, 1, False, False)

        ##################################################
        # Timer for frequency hopping
        ##################################################
        self.hop_timer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self._on_hop_timer, self.hop_timer)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_lora_receiver_0, 'frames'), (self.lora_message_socket_sink_0, 'in'))
        self.connect((self.uhd_usrp_source_0, 0), (self.lora_lora_receiver_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_1, 0))


    # STEP 3: Override the Start method
    def Start(self, *args, **kwargs):
        # STEP 4: Call the parent's Start method FIRST. This starts the
        # actual GNU Radio flowgraph.
        super(single, self).Start(*args, **kwargs)

        # STEP 5: Now, and only now, is it safe to start your custom logic.
        # At this point, __init__ has completed and self.hop_interval exists.
        if hasattr(self, 'hop_interval') and self.hop_interval > 0:
            self.hop_timer.Start(self.hop_interval)

    # It's good practice to also override Stop
    def Stop(self, *args, **kwargs):
        if hasattr(self, 'hop_timer'):
            self.hop_timer.Stop()
        super(single, self).Stop(*args, **kwargs)


    def _on_hop_timer(self, event):
        self.freq_index = (self.freq_index + 1) % len(self.target_freq)
        new_freq = self.target_freq[self.freq_index]
        self.lora_lora_receiver_0.set_frequencies([new_freq])
        print("Hopping to frequency: %.2f MHz" % (new_freq / 1e6))

    # --- (all your getter and setter methods go here) ---


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
