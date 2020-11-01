import unittest
import Twitch

class MyTestCase(unittest.TestCase):
    def test_break_string(self):
        username, msg = Twitch.break_string(":the_aurelius_!the_aurelius_@the_aurelius_.tmi.twitch.tv PRIVMSG #the_aurelius_ :test")
        self.assertEqual(username, "the_aurelius_")
        self.assertEqual(msg, "test")

    def test_image(self):
        valid2 = Twitch.validate_image('test.jpg')
        self.assertEqual(valid2,False)
        valid1 = Twitch.validate_image('the_aurelius_.png')
        self.assertEqual(valid1,True)

if __name__ == '__main__':
    unittest.main()
