import win32api, win32con, time
import threading
from tkinter import *

Time = {
    'SECOND': 1,
    'MINUTE': 60,
    'HOUR': 3600
}

# 获取键的ascii码
def getKeyCode(keyStr):
    key = keyStr.upper()
    if key == 'CTRL':
        return win32con.VK_CONTROL
    elif key == 'ALT':
        return win32con.VK_MENU
    elif key == 'SHIFT':
        return win32con.VK_SHIFT
    else:
        return ord(key)

class SaverGUI():
    '''
    saver界面类
    '''
    def __init__(self, sys):
        root = Tk()
        root.title('SaveAutomator')
        root.geometry('200x100')
        self.startBtn = Button(root, text='开始', command=sys.start)
        self.startBtn.pack(side=TOP, fill='both')
        self.endBtn = Button(root, text='结束', command=sys.end)
        self.endBtn.pack(side=TOP, fill='both')
        root.mainloop()

class SaverSYS():
    '''
    saver操作类
    '''
    # 保存的时间间隔
    interval = 20 * Time['SECOND']
    # 保存键
    savedKeyStr = 'Ctrl+S'
    # 保存操作状态
    isRun = False
    # 模拟按键进行保存操作
    def save(self, keyList):
        print('save')
        keyLen = len(keyList)
        # keydown
        for i in range(keyLen):
            keyCode = getKeyCode(keyList[i])
            win32api.keybd_event(keyCode, 0, 0, 0)
        # keyup
        for i in range(keyLen-1, -1, -1):
            keyCode = getKeyCode(keyList[i])
            win32api.keybd_event(keyCode, 0, win32con.KEYEVENTF_KEYUP, 0)
    # 开始运行        
    def start(self):
        print('start')
        self.isRun = True
        
    # 结束运行
    def end(self):
        print('end')
        self.isRun = False
    # 创建运行线程
    def runThread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.setDaemon(True)
        self.thread.start()
    # 运行
    def run(self):
        while True:
            if self.isRun:
                time.sleep(self.interval)
                self.save(self.savedKeyStr.replace(' ', '').split('+'))
    # 参数配置
    def config(self, **configDict):
        if 'interval' in configDict:
            self.interval = configDict['interval']
        if 'savedKeyStr' in configDict:
            self.savedKeyStr = configDict['savedKeyStr']
        return True

# 主程序
def main():
    # 保存操作类实例
    sysInstance = SaverSYS()
    # 创建运行线程
    sysInstance.runThread()
    # GUI类实例
    SaverGUI(sysInstance)

if __name__ == '__main__':
    main()