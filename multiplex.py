#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lora Receive Realtime
# Generated: Tue Jul 15 13:27:44 2025
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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
from recenter import recenter  # grc-generated hier_block
import lora
import osmosdr
import wx
import pmt

# Custom block to count messages and update the GUI
class MessageCounter(gr.basic_block):
    """
    A block that counts incoming messages, prints the count,
    updates a WX GUI label, and passes the messages through.
    """
    def __init__(self, gui_label):
        gr.basic_block.__init__(self,
            name="Message Counter",
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern('in'))
        self.message_port_register_out(pmt.intern('out'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

        self.gui_label = gui_label
        self.count = 0

    def handle_msg(self, msg):
        """This function is called when a message is received."""
        self.count += 1
        label_text = "LoRa Messages Received: %d" % self.count

        # Use CallAfter for thread-safe GUI updates
        if self.gui_label:
            wx.CallAfter(self.gui_label.SetLabel, label_text)

        print label_text
        self.message_port_pub(pmt.intern('out'), msg)


class lora_receive_realtime(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Lora Receive Realtime")

        ##################################################
        # Variables
        ##################################################
        self.sf = sf = 11
        self.samp_rate = samp_rate = 1e6
        self.bw = bw = 125000
        self.target_freq = target_freq = 910.3e6
        self.symbols_per_sec = symbols_per_sec = float(self.bw) / (2**self.sf)
        self.firdes_tap = firdes_tap = firdes.low_pass(1, self.samp_rate, self.bw, 10000, firdes.WIN_HAMMING, 6.67)
        self.downlink = downlink = False
        self.decimation = decimation = 1
        self.cutoff = cutoff = 500e3
        self.capture_freq = capture_freq = 910e6
        self.bitrate = bitrate = self.sf * (1 / (2**self.sf / float(self.bw)))

        ##################################################
        # Blocks
        ##################################################
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        # FIX: Call SetSizer on the GUI window (self.GetWin()), not the flowgraph (self).
        self.GetWin().SetSizer(self.main_sizer)

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
        self.main_sizer.Add(self.wxgui_fftsink2_1.win, 1, wx.EXPAND)

        self.counter_label = wx.StaticText(self.GetWin(), label="LoRa Messages Received: 0", style=wx.ALIGN_CENTRE)
        self.main_sizer.Add(self.counter_label, 0, wx.ALL | wx.EXPAND, 5)

        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_center_freq(self.capture_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.recenter_0_0_6 = recenter(
            cutoff=self.cutoff,
            decim=1,
            htd_offset=700e3,
            samp_rate0=self.samp_rate,
        )
        self.recenter_0_0_5 = recenter(
            cutoff=self.cutoff,
            decim=1,
            htd_offset=-700e3,
            samp_rate0=self.samp_rate,
        )
        self.recenter_0_0_4 = recenter(
            cutoff=self.cutoff,
            decim=1,
            htd_offset=500e3,
            samp_rate0=self.samp_rate,
        )
        self.recenter_0_0_3 = recenter(
            cutoff=self.cutoff,
            decim=1,
            htd_offset=-500e3,
            samp_rate0=self.samp_rate,
        )
        self.recenter_0_0_2 = recenter(
            cutoff=self.cutoff,
            decim=1,
            htd_offset=300e3,
            samp_rate0=self.samp_rate,
        )
        self.recenter_0_0_1 = recenter(
            cutoff=self.cutoff,
            decim=1,
            htd_offset=-300e3,
            samp_rate0=self.samp_rate,
        )
        self.recenter_0_0_0 = recenter(
            cutoff=self.cutoff,
            decim=1,
            htd_offset=100e3,
            samp_rate0=self.samp_rate,
        )
        self.recenter_0_0 = recenter(
            cutoff=self.cutoff,
            decim=1,
            htd_offset=-100e3,
            samp_rate0=self.samp_rate,
        )
        self.recenter_0 = recenter(
            cutoff=self.cutoff,
            decim=1,
            htd_offset=0,
            samp_rate0=self.samp_rate,
        )
        self.lora_message_socket_sink_0 = lora.message_socket_sink('127.0.0.1', 40868, 0)
        self.lora_lora_receiver_0_0_3 = lora.lora_receiver(1e6, self.capture_freq, ([self.target_freq]), self.bw, 12, False, 4, True, False, self.downlink, self.decimation, False, False)
        self.lora_lora_receiver_0_0_2 = lora.lora_receiver(1e6, self.capture_freq, ([self.target_freq]), self.bw, self.sf, False, 4, True, False, self.downlink, self.decimation, False, False)
        self.lora_lora_receiver_0_0_1 = lora.lora_receiver(1e6, self.capture_freq, ([self.target_freq]), self.bw, 10, False, 4, True, False, self.downlink, self.decimation, False, False)
        self.lora_lora_receiver_0_0_0 = lora.lora_receiver(1e6, self.capture_freq, ([self.target_freq]), self.bw, 9, False, 4, True, False, self.downlink, self.decimation, False, False)
        self.lora_lora_receiver_0_0 = lora.lora_receiver(1e6, self.capture_freq, ([self.target_freq]), self.bw, 8, False, 4, True, False, self.downlink, self.decimation, False, False)
        self.lora_lora_receiver_0 = lora.lora_receiver(1e6, self.capture_freq, ([self.target_freq]), self.bw, 7, False, 4, True, False, self.downlink, self.decimation, False, False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)

        self.message_counter_0 = MessageCounter(self.counter_label)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_lora_receiver_0, 'frames'), (self.message_counter_0, 'in'))
        self.msg_connect((self.lora_lora_receiver_0_0, 'frames'), (self.message_counter_0, 'in'))
        self.msg_connect((self.lora_lora_receiver_0_0_0, 'frames'), (self.message_counter_0, 'in'))
        self.msg_connect((self.lora_lora_receiver_0_0_1, 'frames'), (self.message_counter_0, 'in'))
        self.msg_connect((self.lora_lora_receiver_0_0_2, 'frames'), (self.message_counter_0, 'in'))
        self.msg_connect((self.lora_lora_receiver_0_0_3, 'frames'), (self.message_counter_0, 'in'))

        self.msg_connect((self.message_counter_0, 'out'), (self.lora_message_socket_sink_0, 'in'))

        self.connect((self.blocks_add_xx_0, 0), (self.lora_lora_receiver_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.lora_lora_receiver_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.lora_lora_receiver_0_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.lora_lora_receiver_0_0_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.lora_lora_receiver_0_0_2, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.lora_lora_receiver_0_0_3, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.wxgui_fftsink2_1, 0))
        self.connect((self.recenter_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.recenter_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.recenter_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.recenter_0_0_1, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.recenter_0_0_2, 0), (self.blocks_add_xx_0, 4))
        self.connect((self.recenter_0_0_3, 0), (self.blocks_add_xx_0, 5))
        self.connect((self.recenter_0_0_4, 0), (self.blocks_add_xx_0, 6))
        self.connect((self.recenter_0_0_5, 0), (self.blocks_add_xx_0, 7))
        self.connect((self.recenter_0_0_6, 0), (self.blocks_add_xx_0, 8))
        self.connect((self.rtlsdr_source_0, 0), (self.recenter_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.recenter_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.recenter_0_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.recenter_0_0_1, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.recenter_0_0_2, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.recenter_0_0_3, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.recenter_0_0_4, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.recenter_0_0_5, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.recenter_0_0_6, 0))

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.set_symbols_per_sec(float(self.bw) / (2**self.sf))
        self.lora_lora_receiver_0_0_2.set_sf(self.sf)
        self.set_bitrate(self.sf * (1 / (2**self.sf / float(self.bw))))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.recenter_0_0_6.set_samp_rate0(self.samp_rate)
        self.recenter_0_0_5.set_samp_rate0(self.samp_rate)
        self.recenter_0_0_4.set_samp_rate0(self.samp_rate)
        self.recenter_0_0_3.set_samp_rate0(self.samp_rate)
        self.recenter_0_0_2.set_samp_rate0(self.samp_rate)
        self.recenter_0_0_1.set_samp_rate0(self.samp_rate)
        self.recenter_0_0_0.set_samp_rate0(self.samp_rate)
        self.recenter_0_0.set_samp_rate0(self.samp_rate)
        self.recenter_0.set_samp_rate0(self.samp_rate)
        self.set_firdes_tap(firdes.low_pass(1, self.samp_rate, self.bw, 10000, firdes.WIN_HAMMING, 6.67))

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_symbols_per_sec(float(self.bw) / (2**self.sf))
        self.set_firdes_tap(firdes.low_pass(1, self.samp_rate, self.bw, 10000, firdes.WIN_HAMMING, 6.67))
        self.set_bitrate(self.sf * (1 / (2**self.sf / float(self.bw))))

    def get_target_freq(self):
        return self.target_freq

    def set_target_freq(self, target_freq):
        self.target_freq = target_freq

    def get_symbols_per_sec(self):
        return self.symbols_per_sec

    def set_symbols_per_sec(self, symbols_per_sec):
        self.symbols_per_sec = symbols_per_sec

    def get_firdes_tap(self):
        return self.firdes_tap

    def set_firdes_tap(self, firdes_tap):
        self.firdes_tap = firdes_tap

    def get_downlink(self):
        return self.downlink

    def set_downlink(self, downlink):
        self.downlink = downlink

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        self.recenter_0_0_6.set_cutoff(self.cutoff)
        self.recenter_0_0_5.set_cutoff(self.cutoff)
        self.recenter_0_0_4.set_cutoff(self.cutoff)
        self.recenter_0_0_3.set_cutoff(self.cutoff)
        self.recenter_0_0_2.set_cutoff(self.cutoff)
        self.recenter_0_0_1.set_cutoff(self.cutoff)
        self.recenter_0_0_0.set_cutoff(self.cutoff)
        self.recenter_0_0.set_cutoff(self.cutoff)
        self.recenter_0.set_cutoff(self.cutoff)

    def get_capture_freq(self):
        return self.capture_freq

    def set_capture_freq(self, capture_freq):
        self.capture_freq = capture_freq
        self.wxgui_fftsink2_1.set_baseband_freq(self.capture_freq)
        self.rtlsdr_source_0.set_center_freq(self.capture_freq, 0)

    def get_bitrate(self):
        return self.bitrate

    def set_bitrate(self, bitrate):
        self.bitrate = bitrate


def main(top_block_cls=lora_receive_realtime, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
