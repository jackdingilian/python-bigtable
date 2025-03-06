# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import warnings


class _CRC32C(object):
    """
    Wrapper around ``google_crc32c`` library that logs a warning when it is not available
    on the current architechure.
    """

    def __init__(self):
        try:
            import google_crc32c

            self._google_crc32c = google_crc32c
            self.import_failed = False
        except ImportError:
            self.import_failed = True
            warnings.warn(
                "Unable to import 'google-crc32 library on this python version and architecture."
                " Disabling ExecuteQuery checksum validation. Please upgrade to a supported version",
                " and architecture if possible",
                category=RuntimeWarning,
            )

    def enabled(self) -> bool:
        """
        True whenever ``google_crc32c`` can be imported. False, otherwise.
        """
        return not self.import_failed

    def checksum(self, val: bytearray) -> int:
        """
        Returns the crc32c checksum of the data. ``enabled`` should always be checked before calling.
        """
        # google_crc32c wants bytes. Use a memoryview to avoid a copy
        memory_view = memoryview(val)
        return self._google_crc32c.value(bytes(memory_view))
