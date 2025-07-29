#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Hopping (Corrected)
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
        # Call the parent constructor FIRST.
        grc_wxgui.top_block_gui.__init__(self, title="Hopping")

        ##################################################
        # Variables
        ##################################################
        # Now define all your variables. They will be properly set on the
        # Python object before the Start method is called by the GUI.
        self.sf = sf = 7
        self.samp_rate = samp_rate = 1e6
        self.bw = bw = 125000
        self.target_freq = target_freq = [902.3e6, 902.5e6, 902.7e6, 902.9e6, 903.1e6, 903.3e6, 903.5e6, 903.7e6, 903.9e6, 904.1e6]
        self.hop_interval = hop_interval = 1000 # 1 second
        self.freq_index = freq_index = 0
        self.capture_freq = capture_freq = 903e6
        # ... (other variables) ...

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
        # Connections
        ##################################################
        self.msg_connect((self.lora_lora_receiver_0, 'frames'), (self.lora_message_socket_sink_0, 'in'))
        self.connect((self.uhd_usrp_source_0, 0), (self.lora_lora_receiver_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_1, 0))

        ##################################################
        # Timer for frequency hopping
        ##################################################
        # It's safe to define the timer here, but we will start it in our own Start() method.
        self.hop_timer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self._on_hop_timer, self.hop_timer)

    # This method is called by the parent __init__
    def Start(self, *args, **kwargs):
        # First, call the original Start method from the parent class
        super(single, self).Start(*args, **kwargs)
        # Now that the flowgraph is running, it's safe to start our timer
        if self.hop_interval > 0:
            self.hop_timer.Start(self.hop_interval)

    def Stop(self, *args, **kwargs):
        # It's good practice to stop the timer when the flowgraph stops
        self.hop_timer.Stop()
        super(single, self).Stop(*args, **kwargs)

    def _on_hop_timer(self, event):
        self.freq_index = (self.freq_index + 1) % len(self.target_freq)
        new_freq = self.target_freq[self.freq_index]
        self.lora_lora_receiver_0.set_frequencies([new_freq])
        print("Hopping to frequency: %.2f MHz" % (new_freq / 1e6))

    # --- (rest of your getter/setter methods remain the same) ---


def main(top_block_cls=single, options=None):
    try:
        tb = top_block_cls()
        tb.Start(True)
        tb.Wait()
    except Exception as e:
        # This will catch other potential errors during startup
        print "Error starting flowgraph: %s" % e
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
