import wx
import wx.html2
import winreg
import wx.lib.scrolledpanel as scrolled
import pickle

#ウェブブラウザ作成
class window:

    def __init__(self, url, name):
        self.URL = url
        self.name = name

    #ウェブブラウザを開く
    def open(self):
        #ブラウザをIE11に設定
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
              r"SOFTWARE\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BROWSER_EMULATION", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, 'python.exe', 0, winreg.REG_DWORD, 0x00002af8)
        app = wx.App()
        frame = wx.Frame(None)
        w = wx.html2.WebView.New(frame)
        w.LoadURL(self.URL)
        frame.Show()
        app.MainLoop()

#ボタンの追加
class button_create:
    def __init__(self, tex, tex1, panel, layout):
        self.tex = tex
        self.tex1 = tex1
        self.panel = panel
        self.layout = layout

    def click(self, event):
        def push(event):
            #ウィンドウを開く
            created_window.open()

        created_window = window(self.tex.GetValue(), self.tex1.GetValue())
        created_button = wx.Button(self.panel, wx.ID_ANY, self.tex1.GetValue())

        #配列の保存
        try:
            with open('list.txt', "rb") as f:
                list = pickle.load(f)
                list[1].append(self.tex1.GetValue())
                list[0].append(self.tex.GetValue())
                print(list)

            with open('list.txt', 'wb') as f:
                pickle.dump(list, f)

        except EOFError:
            URL_list = [[self.tex.GetValue()], [self.tex1.GetValue()]]
            with open('list.txt', 'wb') as f:
                pickle.dump(URL_list, f)

        self.tex.SetValue('')
        self.tex1.SetValue('')

        self.layout.Add(created_button, flag=wx.GROW)

        created_button.Bind(wx.EVT_BUTTON, push)

        #レイアウトの更新
        self.layout.Layout()
        #スクロール更新
        self.panel.SetupScrolling()

    #保存されているボタンを作成
    def read(self):
        def push(event):
            created_window.open()

        created_window = window(self.tex, self.tex1)
        created_button = wx.Button(self.panel, wx.ID_ANY, self.tex1)

        self.layout.Add(created_button, flag=wx.GROW)

        created_button.Bind(wx.EVT_BUTTON, push)

        # レイアウトの更新
        self.layout.Layout()
        # スクロール更新
        self.panel.SetupScrolling()

class app :
    def __init__(self):
        app = wx.App()
        frame = wx.Frame(None, wx.ID_ANY, 'Hello,World', size=(200, 400))

        panel = scrolled.ScrolledPanel(frame, wx.ID_ANY)
        panel.SetupScrolling()

        panel.SetBackgroundColour('#AFAFAF')

        text_box = wx.TextCtrl(panel, wx.ID_ANY)
        text_box1 = wx.TextCtrl(panel, wx.ID_ANY)
        #del_number = wx.TextCtrl(panel, wx.ID_ANY)
        button = wx.Button(panel, wx.ID_ANY, '作成')
        #del_button = wx.Button(panel, wx.ID_ANY, '削除')
        layout = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(layout)

        URL = button_create(text_box, text_box1, panel, layout)
        button.Bind(wx.EVT_BUTTON, URL.click)

        layout.Add(text_box, flag=wx.GROW)
        layout.Add(text_box1, flag=wx.GROW)
        layout.Add(button, flag=wx.GROW)
        #layout.Add(del_number, flag=wx.GROW)
        #layout.Add(del_button, flag=wx.GROW)

        #保存されている配列の読み込み
        try:
            with open('list.txt', "rb") as f:
                saved_URL = pickle.load(f)

                for x, x2 in zip(saved_URL[0], saved_URL[1]):
                    button_create(x, x2, panel, layout).read()

        except EOFError:
            print('ファイルが,空じゃあねぇか…!')

        frame.Show()
        app.MainLoop()



app()