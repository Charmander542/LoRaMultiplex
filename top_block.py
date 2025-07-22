#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Jul 22 16:33:58 2025
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
import epy_block_0
import lora
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")

        ##################################################
        # Variables
        ##################################################
        self.channels = channels = 10
        self.ch_rate = ch_rate = 400e3
        self.sf = sf = 11
        self.samp_rate = samp_rate = ch_rate*channels
        self.ch_tb = ch_tb = 20e3
        self.ch_bw = ch_bw = ch_rate/2
        self.bw = bw = 125000
        self.target_freq = target_freq = 910.3e6
        self.taps = taps = firdes.low_pass(1, samp_rate, ch_bw, ch_tb, firdes.WIN_BLACKMAN_hARRIS)
        self.symbols_per_sec = symbols_per_sec = float(bw) / (2**sf)
        self.firdes_tap = firdes_tap = firdes.low_pass(1, samp_rate, bw, 10000, firdes.WIN_HAMMING, 6.67)
        self.downlink = downlink = False
        self.delay = delay = int(150e3)
        self.decimation = decimation = 1
        self.capture_freq = capture_freq = 910.3e6
        self.bitrate = bitrate = sf * (1 / (2**sf / float(bw)))
        self.atten = atten = 60

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("serial: 3134BCA", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(capture_freq, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=5,
                decimation=8,
                taps=(firdes.low_pass(1, 400000, 62500, 20000, firdes.WIN_HAMMING)),
                fractional_bw=None,
        )
        self.pfb_channelizer_ccf_0 = pfb.channelizer_ccf(
        	  channels,
        	  (taps),
        	  1.0,
        	  atten)
        self.pfb_channelizer_ccf_0.set_channel_map(([]))
        self.pfb_channelizer_ccf_0.declare_sample_delay(0)

        self.lora_lora_receiver_0_0_3 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), bw, 12, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_0_2 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), bw, sf, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_0_1 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), bw, 10, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_0_0 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), bw, 9, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0_0 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), bw, 8, False, 4, True, False, downlink, decimation, False, False)
        self.lora_lora_receiver_0 = lora.lora_receiver(1e6, capture_freq, ([target_freq]), bw, 7, False, 4, True, False, downlink, decimation, False, False)
        self.epy_block_0 = epy_block_0.blk(num_channels=10, threshold_db=-60.0, hold_time_s=0.750, samp_rate=ch_rate)
        self.blocks_streams_to_vector_0 = blocks.streams_to_vector(gr.sizeof_float*1, channels)
        self.blocks_delay_0_4 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_delay_0_3_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_delay_0_3 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_delay_0_2_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_delay_0_2 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_delay_0_1_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_delay_0_1 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_complex_to_mag_squared_0_8 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_7 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_6 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_5 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_4 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_3 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_2 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_1 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_streams_to_vector_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_streams_to_vector_0, 1))
        self.connect((self.blocks_complex_to_mag_squared_0_1, 0), (self.blocks_streams_to_vector_0, 2))
        self.connect((self.blocks_complex_to_mag_squared_0_2, 0), (self.blocks_streams_to_vector_0, 3))
        self.connect((self.blocks_complex_to_mag_squared_0_3, 0), (self.blocks_streams_to_vector_0, 4))
        self.connect((self.blocks_complex_to_mag_squared_0_4, 0), (self.blocks_streams_to_vector_0, 5))
        self.connect((self.blocks_complex_to_mag_squared_0_5, 0), (self.blocks_streams_to_vector_0, 6))
        self.connect((self.blocks_complex_to_mag_squared_0_6, 0), (self.blocks_streams_to_vector_0, 7))
        self.connect((self.blocks_complex_to_mag_squared_0_7, 0), (self.blocks_streams_to_vector_0, 8))
        self.connect((self.blocks_complex_to_mag_squared_0_8, 0), (self.blocks_streams_to_vector_0, 9))
        self.connect((self.blocks_delay_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.epy_block_0, 1))
        self.connect((self.blocks_delay_0_0_0, 0), (self.epy_block_0, 6))
        self.connect((self.blocks_delay_0_1, 0), (self.epy_block_0, 2))
        self.connect((self.blocks_delay_0_1_0, 0), (self.epy_block_0, 7))
        self.connect((self.blocks_delay_0_2, 0), (self.epy_block_0, 3))
        self.connect((self.blocks_delay_0_2_0, 0), (self.epy_block_0, 8))
        self.connect((self.blocks_delay_0_3, 0), (self.epy_block_0, 4))
        self.connect((self.blocks_delay_0_3_0, 0), (self.epy_block_0, 9))
        self.connect((self.blocks_delay_0_4, 0), (self.epy_block_0, 5))
        self.connect((self.blocks_streams_to_vector_0, 0), (self.epy_block_0, 10))
        self.connect((self.epy_block_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.epy_block_0, 1), (self.blocks_add_xx_0, 1))
        self.connect((self.epy_block_0, 2), (self.blocks_add_xx_0, 2))
        self.connect((self.epy_block_0, 3), (self.blocks_add_xx_0, 3))
        self.connect((self.epy_block_0, 4), (self.blocks_add_xx_0, 4))
        self.connect((self.epy_block_0, 5), (self.blocks_add_xx_0, 5))
        self.connect((self.epy_block_0, 6), (self.blocks_add_xx_0, 6))
        self.connect((self.epy_block_0, 7), (self.blocks_add_xx_0, 7))
        self.connect((self.epy_block_0, 8), (self.blocks_add_xx_0, 8))
        self.connect((self.epy_block_0, 9), (self.blocks_add_xx_0, 9))
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.blocks_complex_to_mag_squared_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.blocks_complex_to_mag_squared_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.blocks_complex_to_mag_squared_0_3, 0))
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.blocks_complex_to_mag_squared_0_4, 0))
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.blocks_complex_to_mag_squared_0_5, 0))
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.blocks_complex_to_mag_squared_0_6, 0))
        self.connect((self.pfb_channelizer_ccf_0, 8), (self.blocks_complex_to_mag_squared_0_7, 0))
        self.connect((self.pfb_channelizer_ccf_0, 9), (self.blocks_complex_to_mag_squared_0_8, 0))
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.blocks_delay_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.blocks_delay_0_0_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.blocks_delay_0_1, 0))
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.blocks_delay_0_1_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.blocks_delay_0_2, 0))
        self.connect((self.pfb_channelizer_ccf_0, 8), (self.blocks_delay_0_2_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.blocks_delay_0_3, 0))
        self.connect((self.pfb_channelizer_ccf_0, 9), (self.blocks_delay_0_3_0, 0))
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.blocks_delay_0_4, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0_2, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_lora_receiver_0_0_3, 0))
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
        self.epy_block_0.samp_rate = self.ch_rate
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
        self.set_taps(firdes.low_pass(1, self.samp_rate, self.ch_bw, self.ch_tb, firdes.WIN_BLACKMAN_hARRIS))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.set_firdes_tap(firdes.low_pass(1, self.samp_rate, self.bw, 10000, firdes.WIN_HAMMING, 6.67))

    def get_ch_tb(self):
        return self.ch_tb

    def set_ch_tb(self, ch_tb):
        self.ch_tb = ch_tb
        self.set_taps(firdes.low_pass(1, self.samp_rate, self.ch_bw, self.ch_tb, firdes.WIN_BLACKMAN_hARRIS))

    def get_ch_bw(self):
        return self.ch_bw

    def set_ch_bw(self, ch_bw):
        self.ch_bw = ch_bw
        self.set_taps(firdes.low_pass(1, self.samp_rate, self.ch_bw, self.ch_tb, firdes.WIN_BLACKMAN_hARRIS))

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
        self.blocks_delay_0_4.set_dly(self.delay)
        self.blocks_delay_0_3_0.set_dly(self.delay)
        self.blocks_delay_0_3.set_dly(self.delay)
        self.blocks_delay_0_2_0.set_dly(self.delay)
        self.blocks_delay_0_2.set_dly(self.delay)
        self.blocks_delay_0_1_0.set_dly(self.delay)
        self.blocks_delay_0_1.set_dly(self.delay)
        self.blocks_delay_0_0_0.set_dly(self.delay)
        self.blocks_delay_0_0.set_dly(self.delay)
        self.blocks_delay_0.set_dly(self.delay)

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


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
