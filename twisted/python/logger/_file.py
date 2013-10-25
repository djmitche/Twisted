# -*- test-case-name: twisted.python.logger.test.test_file -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
File log observer.
"""

__all__ = [
    "FileLogObserver",
    "textFileLogObserver",
]

from zope.interface import implementer

from twisted.python.compat import ioType, unicode
from twisted.python.logger._observer import ILogObserver
from twisted.python.logger._format import formatTime
from twisted.python.logger._format import timeFormatRFC3339
from twisted.python.logger._format import formatEventAsClassicLogText




@implementer(ILogObserver)
class FileLogObserver(object):
    """
    Log observer that writes to a file-like object.
    """
    def __init__(self, outFile, formatEvent):
        """
        @param outFile: a file-like object.  Ideally one should be passed
            which accepts unicode; if not, utf-8 will be used as the encoding.
        @type outFile: L{io.IOBase}

        @param formatEvent: a callable formats an event
        @type formatEvent: L{callable} that takes an C{event} argument and
            returns a formatted event as L{unicode}.
        """
        if ioType(outFile) is not unicode:
            self._encoding = "utf-8"
        else:
            self._encoding = None
        self._outFile = outFile
        self.formatEvent = formatEvent


    def __call__(self, event):
        """
        Write event to file.

        @param event: an event.
        @type event: L{dict}
        """
        text = self.formatEvent(event)
        if not text:
            return
        if self._encoding is not None:
            text = text.encode(self._encoding)
        self._outFile.write(text)
        self._outFile.flush()



def textFileLogObserver(outFile, timeFormat=timeFormatRFC3339):
    """
    Create a L{FileLogObserver} that emits text to a specified (writable)
    file-like object.

    @param outFile: a file-like object.  Ideally one should be passed
        which accepts unicode; if not, utf-8 will be used as the encoding.
    @type outFile: L{io.IOBase}

    @param timeFormat: the format to use when adding timestamp prefixes to
        logged events.  If C{None}, or for events with no C{"log_timestamp"}
        key, the default timestamp prefix of C{u"-"} is used.
    @type timeFormat: L{unicode} or C{None}

    @return: a file log observer.
    @rtype: L{FileLogObserver}
    """
    def formatEvent(event):
        return formatEventAsClassicLogText(
            event, formatTime=lambda e: formatTime(e, timeFormat)
        )

    return FileLogObserver(outFile, formatEvent)