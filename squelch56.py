#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Squelch56
# Generated: Fri Aug  1 16:04:08 2025
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import lora
import time
import wx


class squelch56(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Squelch56")

        ##################################################
        # Variables
        ##################################################
        self.channels = channels = 50
        self.ch_rate = ch_rate = 200e3
        self.sf = sf = 11
        self.samp_rate = samp_rate = ch_rate*channels
        self.ch_tb = ch_tb = 20e3
        self.ch_bw = ch_bw = ch_rate/2
        self.bw = bw = 125000
        self.thresh = thresh = -90
        self.target_freq = target_freq = 910.3e6
        self.taps = taps = firdes.low_pass(1, samp_rate, ch_bw, ch_tb, firdes.WIN_HAMMING)
        self.symbols_per_sec = symbols_per_sec = float(bw) / (2**sf)
        self.firdes_tap = firdes_tap = firdes.low_pass(1, samp_rate, bw, 10000, firdes.WIN_HAMMING, 6.67)
        self.downlink = downlink = False
        self.delay = delay = int(150e3)
        self.decimation = decimation = 1
        self.capture_freq = capture_freq = 910.3e6
        self.bitrate = bitrate = sf * (1 / (2**sf / float(bw)))
        self.atten = atten = 30

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("serial=3134B8C", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(capture_freq, 0)
        self.uhd_usrp_source_0.set_gain(20, 0)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=5,
                decimation=4,
                taps=(firdes.low_pass(1, 400000, 62500, 20000, firdes.WIN_HAMMING)),
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=5,
                decimation=4,
                taps=(firdes.low_pass(1, 400000, 62500, 20000, firdes.WIN_HAMMING)),
                fractional_bw=None,
        )
        self.pfb_synthesizer_ccf_0_0_3 = filter.pfb_synthesizer_ccf(
        	  4, (), False)
        self.pfb_synthesizer_ccf_0_0_3.set_channel_map(([]))
        self.pfb_synthesizer_ccf_0_0_3.declare_sample_delay(0)

        self.pfb_synthesizer_ccf_0_0_2 = filter.pfb_synthesizer_ccf(
        	  4, (), False)
        self.pfb_synthesizer_ccf_0_0_2.set_channel_map(([]))
        self.pfb_synthesizer_ccf_0_0_2.declare_sample_delay(0)

        self.pfb_synthesizer_ccf_0_0_1 = filter.pfb_synthesizer_ccf(
        	  4, (), False)
        self.pfb_synthesizer_ccf_0_0_1.set_channel_map(([]))
        self.pfb_synthesizer_ccf_0_0_1.declare_sample_delay(0)

        self.pfb_synthesizer_ccf_0_0_0 = filter.pfb_synthesizer_ccf(
        	  4, (), False)
        self.pfb_synthesizer_ccf_0_0_0.set_channel_map(([]))
        self.pfb_synthesizer_ccf_0_0_0.declare_sample_delay(0)

        self.pfb_synthesizer_ccf_0_0 = filter.pfb_synthesizer_ccf(
        	  4, (), False)
        self.pfb_synthesizer_ccf_0_0.set_channel_map(([]))
        self.pfb_synthesizer_ccf_0_0.declare_sample_delay(0)

        self.pfb_synthesizer_ccf_0 = filter.pfb_synthesizer_ccf(
        	  4, (), False)
        self.pfb_synthesizer_ccf_0.set_channel_map(([]))
        self.pfb_synthesizer_ccf_0.declare_sample_delay(0)

        self.pfb_channelizer_ccf_0 = pfb.channelizer_ccf(
        	  channels,
        	  (taps),
        	  1.0,
        	  atten)
        self.pfb_channelizer_ccf_0.set_channel_map(([]))
        self.pfb_channelizer_ccf_0.declare_sample_delay(0)

        self.lora_lora_receiver_0_1_4 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), int(500e3), 12, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_1_3 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), int(500e3), 11, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_1_2 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), int(500e3), 10, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_1_1 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), int(500e3), 9, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_1_0 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), int(500e3), 8, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_1 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), int(500e3), 7, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_0_3 = lora.lora_receiver(250e3, capture_freq, ([target_freq]), bw, 12, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_0_2 = lora.lora_receiver(250e3, capture_freq, ([target_freq]), bw, sf, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_0_1 = lora.lora_receiver(250e3, capture_freq, ([target_freq]), bw, 10, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_0_0 = lora.lora_receiver(250e3, capture_freq, ([target_freq]), bw, 9, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_0 = lora.lora_receiver(250e3, capture_freq, ([target_freq]), bw, 8, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0 = lora.lora_receiver(250e3, capture_freq, ([target_freq]), bw, 7, False, 4, True, False, downlink, decimation, False, False)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_pwr_squelch_xx_0_2_1_4 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_2_1_3 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_2_1_2 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_2_1_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_2_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_2_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_2_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_2 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_4_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_4 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_3_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_3 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_3_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_3 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_2_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_2 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_4_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_4 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_3_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_3 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_2_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_2_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_2_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_2_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_2 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_1_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_1_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_1_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_0_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_0_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_0_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_0_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_0_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_0_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_2 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_1_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_1_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_1_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_0_1_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_0_1 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_0_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(thresh, 1e-4, 0, True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_pwr_squelch_xx_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.analog_pwr_squelch_xx_0_0_0_0, 0), (self.blocks_add_xx_0, 12))
        self.connect((self.analog_pwr_squelch_xx_0_0_0_0_0, 0), (self.blocks_add_xx_0, 32))
        self.connect((self.analog_pwr_squelch_xx_0_0_0_1, 0), (self.blocks_add_xx_0, 22))
        self.connect((self.analog_pwr_squelch_xx_0_0_0_1_0, 0), (self.blocks_add_xx_0, 42))
        self.connect((self.analog_pwr_squelch_xx_0_0_1, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.analog_pwr_squelch_xx_0_0_1_0, 0), (self.blocks_add_xx_0, 13))
        self.connect((self.analog_pwr_squelch_xx_0_0_1_0_0, 0), (self.blocks_add_xx_0, 33))
        self.connect((self.analog_pwr_squelch_xx_0_0_1_1, 0), (self.blocks_add_xx_0, 23))
        self.connect((self.analog_pwr_squelch_xx_0_0_1_1_0, 0), (self.blocks_add_xx_0, 43))
        self.connect((self.analog_pwr_squelch_xx_0_0_2, 0), (self.blocks_add_xx_0, 4))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_0, 0), (self.blocks_add_xx_0, 5))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_0_0, 0), (self.blocks_add_xx_0, 15))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_0_0_0, 0), (self.blocks_add_xx_0, 35))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_0_1, 0), (self.blocks_add_xx_0, 25))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_0_1_0, 0), (self.blocks_add_xx_0, 45))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1, 0), (self.blocks_add_xx_0, 6))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_0, 0), (self.blocks_add_xx_0, 7))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_0_0, 0), (self.blocks_add_xx_0, 17))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_0_0_0, 0), (self.blocks_add_xx_0, 37))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_0_1, 0), (self.blocks_add_xx_0, 27))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_0_1_0, 0), (self.blocks_add_xx_0, 47))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_1, 0), (self.blocks_add_xx_0, 8))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_1_0, 0), (self.blocks_add_xx_0, 18))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_1_0_0, 0), (self.blocks_add_xx_0, 38))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_1_1, 0), (self.blocks_add_xx_0, 28))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_1_1_0, 0), (self.blocks_add_xx_0, 48))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_2, 0), (self.blocks_add_xx_0, 9))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_2_0, 0), (self.blocks_add_xx_0, 19))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_2_0_0, 0), (self.blocks_add_xx_0, 39))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_2_1, 0), (self.blocks_add_xx_0, 29))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_2_1_0, 0), (self.blocks_add_xx_0, 49))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_3, 0), (self.blocks_add_xx_0, 16))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_3_0, 0), (self.blocks_add_xx_0, 36))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_4, 0), (self.blocks_add_xx_0, 26))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_1_4_0, 0), (self.blocks_add_xx_0, 46))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_2, 0), (self.blocks_add_xx_0, 14))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_2_0, 0), (self.blocks_add_xx_0, 34))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_3, 0), (self.blocks_add_xx_0, 24))
        self.connect((self.analog_pwr_squelch_xx_0_0_2_3_0, 0), (self.blocks_add_xx_0, 44))
        self.connect((self.analog_pwr_squelch_xx_0_0_3, 0), (self.blocks_add_xx_0, 11))
        self.connect((self.analog_pwr_squelch_xx_0_0_3_0, 0), (self.blocks_add_xx_0, 31))
        self.connect((self.analog_pwr_squelch_xx_0_0_4, 0), (self.blocks_add_xx_0, 21))
        self.connect((self.analog_pwr_squelch_xx_0_0_4_0, 0), (self.blocks_add_xx_0, 41))
        self.connect((self.analog_pwr_squelch_xx_0_1, 0), (self.blocks_add_xx_0, 10))
        self.connect((self.analog_pwr_squelch_xx_0_1_0, 0), (self.blocks_add_xx_0, 30))
        self.connect((self.analog_pwr_squelch_xx_0_2, 0), (self.blocks_add_xx_0, 20))
        self.connect((self.analog_pwr_squelch_xx_0_2_0, 0), (self.blocks_add_xx_0, 40))
        self.connect((self.analog_pwr_squelch_xx_0_2_1, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.analog_pwr_squelch_xx_0_2_1_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.analog_pwr_squelch_xx_0_2_1_1, 0), (self.blocks_add_xx_1, 2))
        self.connect((self.analog_pwr_squelch_xx_0_2_1_2, 0), (self.blocks_add_xx_1, 3))
        self.connect((self.analog_pwr_squelch_xx_0_2_1_3, 0), (self.blocks_add_xx_1, 4))
        self.connect((self.analog_pwr_squelch_xx_0_2_1_4, 0), (self.blocks_add_xx_1, 5))
        self.connect((self.blocks_add_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.analog_pwr_squelch_xx_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.analog_pwr_squelch_xx_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 12), (self.analog_pwr_squelch_xx_0_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 32), (self.analog_pwr_squelch_xx_0_0_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 22), (self.analog_pwr_squelch_xx_0_0_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 42), (self.analog_pwr_squelch_xx_0_0_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.analog_pwr_squelch_xx_0_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 13), (self.analog_pwr_squelch_xx_0_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 33), (self.analog_pwr_squelch_xx_0_0_1_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 23), (self.analog_pwr_squelch_xx_0_0_1_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 43), (self.analog_pwr_squelch_xx_0_0_1_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.analog_pwr_squelch_xx_0_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.analog_pwr_squelch_xx_0_0_2_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 15), (self.analog_pwr_squelch_xx_0_0_2_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 35), (self.analog_pwr_squelch_xx_0_0_2_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 25), (self.analog_pwr_squelch_xx_0_0_2_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 45), (self.analog_pwr_squelch_xx_0_0_2_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.analog_pwr_squelch_xx_0_0_2_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.analog_pwr_squelch_xx_0_0_2_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 17), (self.analog_pwr_squelch_xx_0_0_2_1_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 37), (self.analog_pwr_squelch_xx_0_0_2_1_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 27), (self.analog_pwr_squelch_xx_0_0_2_1_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 47), (self.analog_pwr_squelch_xx_0_0_2_1_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 8), (self.analog_pwr_squelch_xx_0_0_2_1_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 18), (self.analog_pwr_squelch_xx_0_0_2_1_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 38), (self.analog_pwr_squelch_xx_0_0_2_1_1_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 28), (self.analog_pwr_squelch_xx_0_0_2_1_1_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 48), (self.analog_pwr_squelch_xx_0_0_2_1_1_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 9), (self.analog_pwr_squelch_xx_0_0_2_1_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 19), (self.analog_pwr_squelch_xx_0_0_2_1_2_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 39), (self.analog_pwr_squelch_xx_0_0_2_1_2_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 29), (self.analog_pwr_squelch_xx_0_0_2_1_2_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 49), (self.analog_pwr_squelch_xx_0_0_2_1_2_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 16), (self.analog_pwr_squelch_xx_0_0_2_1_3, 0))
        self.connect((self.pfb_channelizer_ccf_0, 36), (self.analog_pwr_squelch_xx_0_0_2_1_3_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 26), (self.analog_pwr_squelch_xx_0_0_2_1_4, 0))
        self.connect((self.pfb_channelizer_ccf_0, 46), (self.analog_pwr_squelch_xx_0_0_2_1_4_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 14), (self.analog_pwr_squelch_xx_0_0_2_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 34), (self.analog_pwr_squelch_xx_0_0_2_2_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 24), (self.analog_pwr_squelch_xx_0_0_2_3, 0))
        self.connect((self.pfb_channelizer_ccf_0, 44), (self.analog_pwr_squelch_xx_0_0_2_3_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 11), (self.analog_pwr_squelch_xx_0_0_3, 0))
        self.connect((self.pfb_channelizer_ccf_0, 31), (self.analog_pwr_squelch_xx_0_0_3_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 21), (self.analog_pwr_squelch_xx_0_0_4, 0))
        self.connect((self.pfb_channelizer_ccf_0, 41), (self.analog_pwr_squelch_xx_0_0_4_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 10), (self.analog_pwr_squelch_xx_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 30), (self.analog_pwr_squelch_xx_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 20), (self.analog_pwr_squelch_xx_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 40), (self.analog_pwr_squelch_xx_0_2_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.pfb_synthesizer_ccf_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.pfb_synthesizer_ccf_0, 1))
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.pfb_synthesizer_ccf_0, 2))
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.pfb_synthesizer_ccf_0, 3))
        self.connect((self.pfb_channelizer_ccf_0, 10), (self.pfb_synthesizer_ccf_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 11), (self.pfb_synthesizer_ccf_0_0, 1))
        self.connect((self.pfb_channelizer_ccf_0, 12), (self.pfb_synthesizer_ccf_0_0, 2))
        self.connect((self.pfb_channelizer_ccf_0, 13), (self.pfb_synthesizer_ccf_0_0, 3))
        self.connect((self.pfb_channelizer_ccf_0, 26), (self.pfb_synthesizer_ccf_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 27), (self.pfb_synthesizer_ccf_0_0_0, 1))
        self.connect((self.pfb_channelizer_ccf_0, 28), (self.pfb_synthesizer_ccf_0_0_0, 2))
        self.connect((self.pfb_channelizer_ccf_0, 29), (self.pfb_synthesizer_ccf_0_0_0, 3))
        self.connect((self.pfb_channelizer_ccf_0, 34), (self.pfb_synthesizer_ccf_0_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 35), (self.pfb_synthesizer_ccf_0_0_1, 1))
        self.connect((self.pfb_channelizer_ccf_0, 36), (self.pfb_synthesizer_ccf_0_0_1, 2))
        self.connect((self.pfb_channelizer_ccf_0, 37), (self.pfb_synthesizer_ccf_0_0_1, 3))
        self.connect((self.pfb_channelizer_ccf_0, 18), (self.pfb_synthesizer_ccf_0_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 19), (self.pfb_synthesizer_ccf_0_0_2, 1))
        self.connect((self.pfb_channelizer_ccf_0, 20), (self.pfb_synthesizer_ccf_0_0_2, 2))
        self.connect((self.pfb_channelizer_ccf_0, 21), (self.pfb_synthesizer_ccf_0_0_2, 3))
        self.connect((self.pfb_channelizer_ccf_0, 42), (self.pfb_synthesizer_ccf_0_0_3, 0))
        self.connect((self.pfb_channelizer_ccf_0, 43), (self.pfb_synthesizer_ccf_0_0_3, 1))
        self.connect((self.pfb_channelizer_ccf_0, 44), (self.pfb_synthesizer_ccf_0_0_3, 2))
        self.connect((self.pfb_channelizer_ccf_0, 45), (self.pfb_synthesizer_ccf_0_0_3, 3))
        self.connect((self.pfb_synthesizer_ccf_0, 0), (self.analog_pwr_squelch_xx_0_2_1, 0))
        self.connect((self.pfb_synthesizer_ccf_0_0, 0), (self.analog_pwr_squelch_xx_0_2_1_0, 0))
        self.connect((self.pfb_synthesizer_ccf_0_0_0, 0), (self.analog_pwr_squelch_xx_0_2_1_2, 0))
        self.connect((self.pfb_synthesizer_ccf_0_0_1, 0), (self.analog_pwr_squelch_xx_0_2_1_3, 0))
        self.connect((self.pfb_synthesizer_ccf_0_0_2, 0), (self.analog_pwr_squelch_xx_0_2_1_1, 0))
        self.connect((self.pfb_synthesizer_ccf_0_0_3, 0), (self.analog_pwr_squelch_xx_0_2_1_4, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0_2, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0_3, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.lora_lora_receiver_0_1, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.lora_lora_receiver_0_1_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.lora_lora_receiver_0_1_1, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.lora_lora_receiver_0_1_2, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.lora_lora_receiver_0_1_3, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.lora_lora_receiver_0_1_4, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pfb_channelizer_ccf_0, 0))

    def get_channels(self):
        return self.channels

    def set_channels(self, channels):
        self.channels = channels
        self.set_samp_rate(self.ch_rate*self.channels)

    def get_ch_rate(self):
        return self.ch_rate

    def set_ch_rate(self, ch_rate):
        self.ch_rate = ch_rate
        self.set_samp_rate(self.ch_rate*self.channels)
        self.set_ch_bw(self.ch_rate/2)

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
        self.set_taps(firdes.low_pass(1, self.samp_rate, self.ch_bw, self.ch_tb, firdes.WIN_HAMMING))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.set_firdes_tap(firdes.low_pass(1, self.samp_rate, self.bw, 10000, firdes.WIN_HAMMING, 6.67))

    def get_ch_tb(self):
        return self.ch_tb

    def set_ch_tb(self, ch_tb):
        self.ch_tb = ch_tb
        self.set_taps(firdes.low_pass(1, self.samp_rate, self.ch_bw, self.ch_tb, firdes.WIN_HAMMING))

    def get_ch_bw(self):
        return self.ch_bw

    def set_ch_bw(self, ch_bw):
        self.ch_bw = ch_bw
        self.set_taps(firdes.low_pass(1, self.samp_rate, self.ch_bw, self.ch_tb, firdes.WIN_HAMMING))

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_symbols_per_sec(float(self.bw) / (2**self.sf))
        self.set_firdes_tap(firdes.low_pass(1, self.samp_rate, self.bw, 10000, firdes.WIN_HAMMING, 6.67))
        self.set_bitrate(self.sf * (1 / (2**self.sf / float(self.bw))))

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh
        self.analog_pwr_squelch_xx_0_2_1_4.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_2_1_3.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_2_1_2.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_2_1_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_2_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_2_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_2_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_2.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_4_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_4.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_3_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_3.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_3_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_3.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_2_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_2.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_4_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_4.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_3_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_3.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_2_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_2_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_2_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_2_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_2.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_1_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_1_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_1_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_0_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_0_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_0_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_0_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_0_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_0_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_2.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_1_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_1_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_1_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_0_1_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_0_1.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_0_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0_0.set_threshold(self.thresh)
        self.analog_pwr_squelch_xx_0.set_threshold(self.thresh)

    def get_target_freq(self):
        return self.target_freq

    def set_target_freq(self, target_freq):
        self.target_freq = target_freq

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.pfb_channelizer_ccf_0.set_taps((self.taps))

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

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation

    def get_capture_freq(self):
        return self.capture_freq

    def set_capture_freq(self, capture_freq):
        self.capture_freq = capture_freq
        self.uhd_usrp_source_0.set_center_freq(self.capture_freq, 0)

    def get_bitrate(self):
        return self.bitrate

    def set_bitrate(self, bitrate):
        self.bitrate = bitrate

    def get_atten(self):
        return self.atten

    def set_atten(self, atten):
        self.atten = atten


def main(top_block_cls=squelch56, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
