import csv

import wx

import mysql.connector

import json

with open('config.json') as json_config:
    config = json.load(json_config)
    json_config.close()

conn = mysql.connector.connect(host = config["host"], port = config["port"], user = config["user"], password = config["password"], database = config["database"])
cursor = conn.cursor()

class Window(wx.Frame):
    def __init__(self, title):
        super().__init__(parent = None, title = title)
        self.panel = wx.Panel(self)
        self.items = []


        self.wrapper = wx.BoxSizer(wx.VERTICAL)
        cursor.execute("show tables")
        for r in cursor.fetchall():
            sizer = wx.FlexGridSizer(rows = 1, cols=2, vgap=5, hgap=5)
            cb = wx.CheckBox(self.panel, name = r[0])
            sizer.AddMany([cb, (wx.StaticText(self.panel, label = r[0]))])
            self.wrapper.Add(sizer, flag = wx.ALL | wx.EXPAND, border = 15)
            self.items.append(cb)

        self.panel.SetSizer(self.wrapper)

        save = wx.Button(self.panel, label = "SAVE", pos = (70, 300), size = (80, 40))
        save.Bind(wx.EVT_BUTTON, self.SAVE)
        exit = wx.Button(self.panel, label = "EXIT", pos = (250, 300), size = (80, 40))
        exit.Bind(wx.EVT_BUTTON, self.EXIT)


        self.SetSize(400, 400)

        self.Centre()
        self.Show()

    def SAVE(self, e):
        for x in self.items:
            if x.GetValue() is True:
                selectquery = (f"SELECT * from {x.GetName()}")
                cursor.execute(selectquery)
                records = cursor.fetchall()
                with open(f'{x.GetName()}.csv', 'w', newline='', encoding="utf-16") as fp:
                    writer = csv.writer(fp, delimiter='\t')

                    for x in records:
                        writer.writerow(x)

                    fp.close()

        conn.close()
        self.Close()

    def EXIT(self, e):
        self.Close()
        conn.close()

app = wx.App()
window = Window("Adatbázis konverter")
app.MainLoop()