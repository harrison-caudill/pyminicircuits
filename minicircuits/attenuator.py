# Copyright (c) 2015, Spire Global Inc
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Spire Global Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# Spire Global Inc BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


import logging
import sys
import usb.core


"""Interface for Mini-Circuits digital attenuators.

This module contains the classes and methods necessary to interact
with the Mini-Circuits line of USB/Ethernet digital attenuators.

NOTE: This software is still considered alpha, and was written
specifically to interact with the RCDAT-4000-120.
"""

from . import USB_VENDOR_ID

__author__ = "Harrison Caudill"
__copyright__ = "Copyright 2015, "
__credits__ = ["Spire Global Inc"]
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Harrison Caudill"
__email__ = "harrison@spire.com"
__status__ = "Alpha"


class DigitalAttenuator(object):
    """Interface to the MiniCircuits digital attenuators.
    """

    PRODUCT_IDS = {
        'RCDAT-4000-120': 0x0023,
        }

    ENDPOINT_READ = 0x81
    ENDPOINT_WRITE = 0x1

    def __init__(self, product_id, bus='usb'):
        assert('usb' == bus)

        # find the device
        self.hid_device = usb.core.find(idVendor=USB_VENDOR_ID,
                                        idProduct=product_id)
        if not self.hid_device:
            msg = "Failed to find device: vendor=%#x id=%#x" % (
                USB_VENDOR_ID, product_id)
            logging.error(msg)
            raise Exception(msg)
        logging.info("Found Device")

        # if necessary, detach it from the kernel's driver
        if self.hid_device.is_kernel_driver_active(0):
            logging.info("Kernel driver is currently attached")
            self.hid_device.detach_kernel_driver(0)

        # Prepare the device for operation
        self.hid_device.set_configuration()
        self.hid_device.reset()

    def _run_cmd(self, cmd, read_len=64):
        assert(len(cmd) <= 64)
        pad_len = 64 - len(cmd)
        pkt = cmd + [ 0 for i in range(pad_len) ]
        self.hid_device.write(self.ENDPOINT_WRITE, pkt)

        return self.hid_device.read(self.ENDPOINT_READ, 64)

    def get_att(self):
        tmp = self._run_cmd([18], read_len=3)
        return tmp[1] + tmp[2]/4.0

    def set_att(self, att):
        cmd = [19, int(att), int((att % 1) / 4.0)]
        tmp = self._run_cmd(cmd, read_len=1)

    def _get_string(self, cmd):
        tmp = self._run_cmd(cmd)
        try:
            tmp = tmp[1:tmp.index(0)]
        except ValueError:
            tmp = tmp[1:]
        return ''.join([chr(b) for b in tmp])

    def get_model(self):
        return self._get_string([40])

    def get_serial(self):
        return self._get_string([41])

    def get_firmware_rev(self):
        tmp = self._run_cmd([99], read_len=7)
        return ''.join([str(b) for b in tmp[5:6]])
