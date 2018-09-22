#
# Copyright (C) 2016 TUDelft
#
# This file is part of paparazzi.
#
# paparazzi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# paparazzi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with paparazzi.  If not, see <http://www.gnu.org/licenses/>.
#

import wx

import sys
import os
import math

PPRZ_HOME = os.getenv("PAPARAZZI_HOME", os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                    '../../../..')))
PPRZ_SRC = os.getenv("PAPARAZZI_SRC", os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                    '../../../..')))

sys.path.append(PPRZ_HOME + "/var/lib/python")

from pprzlink.ivy import IvyMessagesInterface

WIDTH = 300.0
BARH = 140.0

MAX_AIRSPEED = 35.0

MSG_BUFFER_SIZE = 1000

class WindFrame(wx.Frame):
    def message_recv(self, ac_id, msg):
        if msg.name == "ROTORCRAFT_FP":
            self.ground_gs_x[self.count_gs] = float(msg['veast'])
            self.ground_gs_y[self.count_gs] = float(msg['vnorth'])
            self.last_heading = float(msg['psi'])
            self.count_gs = self.count_gs + 1
            if self.count_gs > MSG_BUFFER_SIZE:
                self.count_gs = 0
            wx.CallAfter(self.update)

        elif msg.name =="AIR_DATA":
            self.airspeed[self.count_as] = float(msg['airspeed'])
            self.heading[self.count_as] = self.last_heading
            self.count_as = self.count_as + 1
            if self.count_as > MSG_BUFFER_SIZE:
                self.count_as = 0
            wx.CallAfter(self.update)

    def update(self):
        self.Refresh()

    def OnSize(self, event):
        self.w = event.GetSize().x
        self.h = event.GetSize().y
        self.cfg.Write("width", str(self.w));
        self.cfg.Write("height", str(self.h));
        self.Refresh()

    def OnMove(self, event):
        self.x = event.GetPosition().x
        self.y = event.GetPosition().y
        self.cfg.Write("left", str(self.x));
        self.cfg.Write("top", str(self.y));


    def OnClickD(self,event):
        self.click_on = 1

    def OnClickU(self,event):
        self.click_on = 0

    def OnClickM(self,event):
        if self.click_on == 1:
            m = event.GetPosition().Get()
            self.click_x = m[0] - self.mid
            self.click_y = m[1] - self.mid
            self.Refresh()

    def OnPaint(self, e):

        w = float(self.w)
        h = float(self.h)

        if h/w < (WIDTH / (WIDTH+BARH)):
            w = (WIDTH / (WIDTH+BARH)) * h
        else:
            h = ((WIDTH+BARH) / (WIDTH)) * w

        bar = BARH / WIDTH * w

        tdx = -5
        tdy = -7
        th = 15.0 / WIDTH * w

        dc = wx.PaintDC(self)
        brush = wx.Brush("white")
        dc.SetBackground(brush)
        dc.Clear()

        self.mid = w/2
        diameter = w/2

        # Background
        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0), wx.TRANSPARENT))

        for v in range(0,40,5):
            dc.DrawCircle(self.mid, self.mid, diameter * v / MAX_AIRSPEED )

        font = wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)

        dc.DrawText("N", self.mid + tdx, 2)
        dc.DrawText("S", self.mid + tdx, w - 17)
        dc.DrawText("E", w - 15, w / 2 + tdy)
        dc.DrawText("W", 2, w / 2 + tdy)

        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 255), wx.SOLID))
        for i in range(0,MSG_BUFFER_SIZE):
            gx = self.ground_gs_x[i]
            gy = self.ground_gs_y[i]

            #dc.DrawLine(gx,gy,gx,gy)
            dc.DrawCircle(int(gx+self.mid+self.click_x), int(gy+self.mid+self.click_y), 2)

        dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0), wx.SOLID))
        for i in range(0,MSG_BUFFER_SIZE):
            gx = self.airspeed[i] * math.cos(0)
            gy = self.airspeed[i] * math.sin(0)

            #dc.DrawLine(gx,gy,gx,gy)
            dc.DrawCircle(int(gx+self.mid), int(gy+self.mid), 2)


        font = wx.Font(8, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        dc.DrawText("#" + str(self.count_gs) + ", " + str(self.count_as) + " | " + str(self.click_x) + "-" + str(self.click_y), 0, w + tdy)

        windspeed = math.sqrt(self.click_x * +self.click_x + +self.click_y * +self.click_y) / diameter * MAX_AIRSPEED
        windheading = math.atan2(self.click_x,-self.click_y) * 180 / math.pi
        dc.DrawText("Windspeed = " + str(round(windspeed,2)) + " m/s  form " + str(round(windheading, 1)), 0, w + tdy + th)

        # SV
#            y = float(w) / 2.0 - math.cos(az) * el
#            x = float(w) / 2.0 + math.sin(az) * el

#            dc.SetBrush(wx.Brush(c, wx.SOLID))
#            dc.DrawCircle(int(x), int(y), s)

#            font = wx.Font(8, wx.ROMAN, wx.NORMAL, wx.NORMAL)
#            dc.SetFont(font)
#            dc.DrawText(str(sv.SVID), x + tdx, y + tdy)

#            bh = float(bar - th - th) * float(sv.CNO) / 55.0
#            dc.DrawRectangle(w / CHANNEL * chn + 5 * (1 - used), self.h - th - bh, w / CHANNEL - 2 - 10 * (1 - used), bh)
#            dc.DrawText(str(chn), w / CHANNEL * chn, self.h - th)
#            dc.DrawText(str(sv.CNO), w / CHANNEL * chn, self.h - bar)

    def __init__(self):
        # own data
        self.count_gs = 0
        self.ground_gs_x = [0] * MSG_BUFFER_SIZE
        self.ground_gs_y = [0] * MSG_BUFFER_SIZE

        self.count_as = 0
        self.last_heading = 0;
        self.airspeed = [0] * MSG_BUFFER_SIZE
        self.heading  = [0] * MSG_BUFFER_SIZE

        # Click
        self.click_x = 0
        self.click_y = 0
        self.click_on = 0

        # window
        self.w = WIDTH
        self.h = WIDTH + BARH

        self.cfg = wx.Config('wind_conf')
        if self.cfg.Exists('width'):
            self.w = int(self.cfg.Read('width'))
            self.h = int(self.cfg.Read('height'))

        self.mid = self.w/2

        wx.Frame.__init__(self, id=-1, parent=None, name=u'WindFrame',
                          size=wx.Size(self.w, self.h), title=u'Wind Tool')

        if self.cfg.Exists('left'):
            self.x = int(self.cfg.Read('left'))
            self.y = int(self.cfg.Read('top'))
            self.SetPosition(wx.Point(self.x,self.y), wx.SIZE_USE_EXISTING)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOVE, self.OnMove)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClickD) #EVT_LEFT_DOWN
        self.Bind(wx.EVT_MOTION, self.OnClickM) #EVT_LEFT_DOWN
        self.Bind(wx.EVT_LEFT_UP, self.OnClickU) #EVT_LEFT_DOWN

        #self.Bind( wx.EVT_BUTTON, self.OnButton, btn1 )

        ico = wx.Icon(PPRZ_SRC + "/sw/ground_segment/python/wind/wind.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        self.interface = IvyMessagesInterface("windframe")
        self.interface.subscribe(self.message_recv)

    def OnClose(self, event):
        self.interface.shutdown()
        self.Destroy()
