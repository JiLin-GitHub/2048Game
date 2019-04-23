#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import copy
import random

VALUE_COLOR_DEF = {
            0: "#CCC0B3",
            2: "#EEE4DA",
            4: "#EEE2D0",
            8: "#F2B179",
            16: "#FFEC8B",
            32: "#F59563",
            64: "#F65E3B",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#ECC641",
            2048: "#EDC22E",
            4096: "#EE7621",
            8192: "#F0FFFF",
            16384: "#F0FFF0",
            32768: "#E6E6FA"
        }

class GameFrame(wx.Frame):
    def __init__(self, title):
        self.score = 0
        self.record = 0
        self.first_inited = True
        self.tile_values = [[0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]]
        self.panel_orig_point = wx.Point(20, 100)
        super().__init__(None, title=title, size=(505, 600), style=wx.DEFAULT_FRAME_STYLE)
        self.addWidgets()
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_KEY_DOWN,self.onKey)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetFocus()
    def addWidgets(self):
        self.label_score_text = wx.StaticText(self, -1, u"得分", (200, 15), (80, 30), wx.ALIGN_CENTER)
        self.label_score_text.Font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, faceName=u"Roboto")
        self.label_score_text.SetForegroundColour("#CD661D")
        self.label_score_text.SetBackgroundColour("#FAF8EF")

        self.score_text = wx.StaticText(self, -1, "0", (200, 50), (80, 30), wx.ALIGN_CENTER)
        self.score_text.Font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, faceName=u"Roboto")
        self.score_text.SetForegroundColour("#FFFFFF")

        self.label_record_text = wx.StaticText(self, -1, u"纪录", (300, 15), (80, 30), wx.ALIGN_CENTER)
        self.label_record_text.Font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, faceName=u"Roboto")
        self.label_record_text.SetForegroundColour("#CD661D")
        self.label_record_text.SetBackgroundColour("#FAF8EF")

        self.record_text = wx.StaticText(self, -1, str(self.record), (300, 50), (80, 30), wx.ALIGN_CENTER)
        self.record_text.Font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, faceName=u"Roboto")
        self.record_text.SetForegroundColour("#FFFFFF")

        self.restart_btn = wx.Button(self, -1, u"重新\n开始", (400, 15), (52, 65), wx.ALIGN_CENTER)
        self.restart_btn.Font = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD, faceName=u"Roboto")
        self.restart_btn.SetForegroundColour("#CD661D")
        self.restart_btn.Bind(wx.EVT_BUTTON, self.onBtnRestart)

        self.brand = wx.Image("2048.jpg", type=wx.BITMAP_TYPE_ANY).Rescale(55,55)
        self.brand.SetMask(hasMask=True)
        self.brand_rot = self.brand.Rotate(angle=0.25, rotationCentre=(0,0),interpolating=True)
        self.brand_rot= self.brand_rot.ConvertToBitmap()
        self.brand = wx.StaticBitmap(parent=self, bitmap=self.brand_rot,pos=(25,5),size=(90,90))
        self.brand.SetBackgroundColour("#FAF8EF")

        self.girl = wx.Image('girl.png', type=wx.BITMAP_TYPE_ANY).Rescale(60,85).ConvertToBitmap()
        self.girl = wx.StaticBitmap(parent=self, bitmap=self.girl,pos=(110,3),size=(60,85))
        self.girl.SetBackgroundColour("#FAF8EF")

    def onPaint(self, event):
        if self.first_inited:
            self.first_inited = False
            self.startGame()
        else:
            self.startGameMiniWindow()

    def startGame(self):
        self.tile_values = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.score = 0
        try:
            with open("record.txt") as fp:
                self.record = int(fp.read())
        except (IOError, ValueError) as err:
            print("read record error: %s" % err)
            self.record = 0

        self.addRandomTile()
        self.initScreen()
        self.drawTiles()

    def startGameMiniWindow(self):
        self.initScreen()
        self.drawTiles()

    def initScreen(self):
        dc = wx.ClientDC(self)
        dc.SetBackground(wx.Brush("#FAF8EF"))
        dc.Clear()
        dc.SetBrush(wx.Brush("#C0B0A0"))
        dc.SetPen(wx.Pen("", 1, wx.TRANSPARENT))
        dc.DrawRoundedRectangle(self.panel_orig_point.x, self.panel_orig_point.y, 450, 450, 5)

        self.score_text.SetLabel("0")
        self.record_text.SetLabel(str(self.record))

    def drawTiles(self):
        dc = wx.ClientDC(self)
        dc.SetBrush(wx.Brush("#C0B0A0"))
        dc.SetPen(wx.Pen("", 1, wx.TRANSPARENT))
        dc.DrawRoundedRectangle(self.panel_orig_point.x, self.panel_orig_point.y, 450, 450, 5)
        for row in range(4):
            for column in range(4):
                tile_value = self.tile_values[row][column]
                tile_color = VALUE_COLOR_DEF[tile_value]
                dc.SetBrush(wx.Brush(tile_color))
                dc.DrawRoundedRectangle(self.panel_orig_point.x + 110 * column + 10,
                                        self.panel_orig_point.y + 110 * row + 10, 100, 100, 5)
                dc.SetTextForeground("#707070")
                text_font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.BOLD, faceName=u"Roboto")
                dc.SetFont(text_font)
                if tile_value != 0:
                    size = dc.GetTextExtent(str(tile_value))
                    if size[0] > 100:
                        text_font = wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD, faceName=u"Roboto")
                        dc.SetFont(text_font)
                        size = dc.GetTextExtent(str(tile_value))
                    dc.DrawText(str(tile_value), self.panel_orig_point.x + 110 * column + 10 + (100 - size[0]) / 2,
                                self.panel_orig_point.y + 110 * row + 10 + (100 - size[1]) / 2)

    def onKey(self,event):
        key_code = event.GetKeyCode()
        temp_tile_values = copy.deepcopy(self.tile_values)
        if key_code == wx.WXK_UP:
            self.onKeyUp()
        elif key_code == wx.WXK_DOWN:
            self.onKeyDown()
        elif key_code == wx.WXK_LEFT:
            self.onKeyLeft()
        elif key_code == wx.WXK_RIGHT:
            self.onKeyRight()
        elif key_code == wx.WXK_F1:
            self.tile_values = [[0, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [4096, 8192, 16384, 32768]]
            self.drawTiles()
            return

        if temp_tile_values == self.tile_values:
            if self.isGameOver():
                self.onBtnRestart()
        else:
            self.addRandomTile()
            self.drawTiles()
            self.score_text.SetLabel(str(self.score))

    def onKeyUp(self):
        temp_tile_values = [[row[i] for row in self.tile_values] for i in range(len(self.tile_values[0]))]
        for row in range(len(self.tile_values[0])):
            temp_tile_values[row] = self.updateSingleRowValue(temp_tile_values[row], True)
        self.tile_values = [[row[i] for row in temp_tile_values] for i in range(len(temp_tile_values[0]))]

    def onKeyDown(self):
        temp_tile_values = [[row[i] for row in self.tile_values] for i in range(len(self.tile_values[0]))]
        for row in range(len(self.tile_values[0])):
            temp_tile_values[row] = self.updateSingleRowValue(temp_tile_values[row], False)
        self.tile_values = [[row[i] for row in temp_tile_values] for i in range(len(temp_tile_values[0]))]

    def onKeyLeft(self):
        for row in range(len(self.tile_values)):
            self.tile_values[row] = self.updateSingleRowValue(self.tile_values[row], True)

    def onKeyRight(self):
        for row in range(len(self.tile_values)):
            self.tile_values[row] = self.updateSingleRowValue(self.tile_values[row], False)

    def updateSingleRowValue(self, row_value, positive):
        num_cols = len(row_value)
        if not positive:
            temp_data = copy.deepcopy(row_value)
            row_value = [temp_data[num_cols - 1 - i] for i in range(num_cols)]
        for i in range(num_cols-1):
            if row_value[i] == 0:
                continue
            for j in range(i+1,num_cols):
                if row_value[j]==0:
                    continue
                elif row_value[i]!=row_value[j]:
                    break
                elif (row_value[i]==row_value[j]):
                    self.score += row_value[i]
                    row_value[i] *= 2
                    row_value[j] = 0
                    break

        for i in range(num_cols):
            if row_value[i] != 0:
                continue
            for j in range(i + 1, num_cols):
                if row_value[j] != 0:
                    row_value[i] = row_value[j]
                    row_value[j] = 0
                    break
        if not positive:
            temp_data = copy.deepcopy(row_value)
            row_value = [temp_data[num_cols - 1 - i] for i in range(num_cols)]
        return row_value

    def addRandomTile(self):
        empty_tiles = [(row, col) for row in range(len(self.tile_values)) for col in range(len(self.tile_values[0]))
                       if self.tile_values[row][col] == 0]
        if len(empty_tiles) != 0:
            row, col = empty_tiles[random.randint(0, len(empty_tiles) - 1)]
            # value should be 2 or 4
            self.tile_values[row][col] = 2 ** random.randint(1, 2)
            return True
        else:
            return False

    def isGameOver(self):
        num_rows = len(self.tile_values)
        num_cols = len(self.tile_values[0])
        for i in range(num_rows):
            for j in range(num_cols):
                if self.tile_values[i][j] == 0 or \
                        (j < num_cols - 1 and self.tile_values[i][j] == self.tile_values[i][j + 1]) or \
                        (i < num_rows - 1 and self.tile_values[i][j] == self.tile_values[i + 1][j]):
                    return False
        return True

    def onBtnRestart(self, event):
        if self.score > self.record:
            self.record = self.score
            try:
                with open("record.txt", "w") as fp:
                    fp.write(str(self.score))
            except IOError as err:
                print(err)
        if wx.MessageBox(u"游戏结束，是否重新开始？", u"Game Over", wx.YES_NO) == wx.YES:
            self.startGame()

    def onClose(self,e):
        if wx.MessageBox(u"是否退出游戏并保存纪录？", u"Game Exit", wx.YES_NO) == wx.YES:
            if self.score > self.record:
                self.record = self.score
                try:
                    with open("record.txt", "w") as fp:
                        fp.write(str(self.score))
                except IOError as err:
                    print(err)
            self.Destroy()

class GameApp(wx.App):
    def OnInit(self):
        frame = GameFrame('2048')
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = GameApp()
    app.MainLoop()
