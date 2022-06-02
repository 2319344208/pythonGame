<<<<<<< HEAD


=======
import unittest
from unittest import TestCase
import win32api

import win32con
from unittest.mock import Mock
from pymouse import PyMouse
from alien_invasion import AlienInvasion
class Test(TestCase):

    def test_up(self):
        """按向上键，松向上键测试"""
        ai = AlienInvasion()
        # 创建模拟对象 使用 return_value 指定返回对象
        mock_g = Mock(return_value=ai)
        mock_obj = mock_g()
        """按向上键"""
        # 第一个参数为虚拟键码 第三参数为按键类型，设置为0即为按下
        win32api.keybd_event(38, 0, 0, 0)
        # 持续一段时间
        for i in range(1000):
            # 检查事件
            mock_obj._check_events()
            # 更新飞船位置
            mock_obj.ship.update()

        # 按向上键后moving_up是否变为True
        self.assertEqual(mock_obj.ship.moving_up, True)
        # 按向上键后飞船是否超过边界
        self.assertEqual(mock_obj.ship.rect.y, 0)
        """松开向上键"""
        # 第三参数为按键类型，设置为win32con.KEYEVENTF_KEYUP（2）即为松开
        win32api.keybd_event(38, 0, win32con.KEYEVENTF_KEYUP, 0)
        mock_obj._check_events()
        mock_obj.ship.update()
        # 松开上键后moving_up是否变为False
        self.assertEqual(mock_obj.ship.moving_up, False)

    def test_down(self):
        """按向下键，松向下键测试"""
        ai = AlienInvasion()
        mock_g = Mock(return_value=ai)
        mock_obj = mock_g()
        """按向下键"""
        win32api.keybd_event(40, 0, 0, 0)
        for i in range(1000):
            mock_obj._check_events()
            mock_obj.ship.update()
        # 按向下键后moving_down是否变为True
        self.assertEqual(mock_obj.ship.moving_down, True)
        # 按向下键后飞船是否超过边界
        self.assertEqual(mock_obj.ship.rect.bottom,
                         mock_obj.screen.get_rect().bottom)
        """松开向下键"""
        win32api.keybd_event(40, 0, win32con.KEYEVENTF_KEYUP, 0)
        mock_obj._check_events()
        mock_obj.ship.update()
        # 松开上键后moving_down是否变为False
        self.assertEqual(mock_obj.ship.moving_down, False)

    def test_space(self):
        """按空格键测试"""
        ai = AlienInvasion()
        mock_g = Mock(return_value=ai)
        mock_obj = mock_g()
        """按空格键"""
        # 第二个参数为空格按下的硬件扫描码
        win32api.keybd_event(32, 0x39, 0, 0)
        mock_obj._check_events()
        # 按向下空格键后子弹是否产生
        self.assertEqual(len(mock_obj.bullets), 1)


    def test_click(self):
        ai = AlienInvasion()
        mock_g = Mock(return_value=ai)
        mock_obj = mock_g()

        # 初始值
        self.assertEqual(mock_obj.stats.game_active, False)
        """点击鼠标"""
        m = PyMouse()
        # 点击位置
        m.click(mock_obj.play_button.rect.x, mock_obj.play_button.rect.y)
        mock_obj._check_events()
        # 鼠标点击是否成功
        self.assertEqual(mock_obj.stats.game_active, True)


if __name__ == '__main__':
    unittest.main()
>>>>>>> 90f4ada (seven commit)
