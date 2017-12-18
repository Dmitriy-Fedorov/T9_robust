import unittest
from Desk import T9Desk


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.env = T9Desk()

    def test_action_space(self):
        self.assertEqual(self.env.get_action_space()['p1'].size, self.env.cell_size)
        self.assertEqual(self.env.get_action_space()['p2'].size, self.env.cell_size)
        self.env.tuzdyk['p2'] = 0
        self.assertEqual(self.env.get_action_space()['p2'].size, self.env.cell_size)
        self.env.tuzdyk['p2'] = 1
        self.assertNotEqual(self.env.cell_size, self.env.get_action_space()['p1'].size)
        self.assertEqual(self.env.get_action_space()['p2'].size, self.env.cell_size)
        self.env.desk['p2'][1] = 0
        # print("p1:", self.env.get_action_space()['p1'])
        # print("p2:", self.env.get_action_space()['p2'])
        self.assertEqual(self.env.cell_size-1, self.env.get_action_space()['p2'].size)
        # TODO: check with step, tuzdyk, move

    def test_get_dest_cell(self):
        print('test_get_dest_cell')
        self.assertEqual(9, self.env.cell_size, 'this test is designed for standard board size')
        self.assertEqual(-self.env.cell_size, self.env.get_dest_cell(1))
        for i in range(2, self.env.cell_size):
            self.assertEqual(i-1, self.env.get_dest_cell(i))
        self.env.desk['p1'][0] = 1
        self.assertEqual(-2, self.env.get_dest_cell(1))
        self.env.desk['p1'][0] = 0
        self.assertEqual(-1, self.env.get_dest_cell(1))
        self.env.desk['p1'][self.env.cell_size-1] = 1
        self.assertEqual(1, self.env.get_dest_cell(self.env.cell_size))
        self.env.desk['p1'][3] = self.env.cell_size * 2
        self.assertEqual(-3, self.env.get_dest_cell(4))
        self.env.desk['p1'][3] = self.env.cell_size * 4
        self.assertEqual(-3, self.env.get_dest_cell(4))
        self.env.desk['p1'][3] = self.env.cell_size * 4 + 7
        self.assertEqual(1, self.env.get_dest_cell(4))
        self.assertEqual(1, self.env.dest_cell)

    def test_distribute_balls_iterative(self):
        self.assertEqual(9, self.env.cell_size, 'this test is designed for standard board size')
        env = self.env
        ball_sum = env.desk['p1'].sum() + env.desk['p2'].sum()
        env.distribute_balls_iterative(1)
        env.distribute_balls_iterative(1)
        env.distribute_balls_iterative(3)
        env.distribute_balls_iterative(9)
        env.distribute_balls_iterative(9)
        self.assertEqual(ball_sum, env.desk['p1'].sum() + env.desk['p2'].sum())
        env.who_move = ~env.who_move
        env.distribute_balls_iterative(1)
        env.distribute_balls_iterative(1)
        env.distribute_balls_iterative(9)
        env.distribute_balls_iterative(9)
        # print('sum before: {}, after: {}'.format(ball_sum, env.desk['p1'].sum() + env.desk['p2'].sum()))
        self.assertEqual(ball_sum, env.desk['p1'].sum() + env.desk['p2'].sum())

    def test_set_tuzdyk(self):
        env = self.env
        env.reset()
        self.assertEqual(-1, env.tuzdyk['p1'])
        env.set_tuzdyk(1)
        self.assertEqual(-1, env.tuzdyk['p1'])
        env.desk['p2'][0] = 3
        env.set_tuzdyk(1)
        self.assertEqual(1, env.tuzdyk['p1'])
        env.desk['p2'][1] = 3
        env.set_tuzdyk(2)
        self.assertEqual(1, env.tuzdyk['p1'])

        env.who_move = ~env.who_move
        env.desk['p1'][env.cell_size-1] = 3
        env.set_tuzdyk(env.cell_size)
        self.assertEqual(-2, env.tuzdyk['p2'])
        env.desk['p1'][0] = 3
        env.set_tuzdyk(1)
        self.assertEqual(-2, env.tuzdyk['p2'])
        env.desk['p1'][1] = 3
        env.set_tuzdyk(2)
        self.assertEqual(2, env.tuzdyk['p2'])

    def test_take_tuzdyk(self):
        env = self.env
        ball_sum, total_sum = env.ball_sum()
        env.tuzdyk['p1'] = 5
        env.take_tuzdyk()
        self.assertEqual(0, env.desk['p2'][4])
        self.assertNotEqual(ball_sum, env.ball_sum()[0])
        self.assertEqual(total_sum, env.ball_sum()[1])

    def test_move(self):
        env = self.env
        ball_sum, total_sum = env.ball_sum()
        env.move(2)
        env.who_move = ~env.who_move
        # take_ball check
        self.assertNotEqual(ball_sum, env.ball_sum()[0])
        self.assertEqual(total_sum, env.ball_sum()[1])
        # tuzdyk check
        env.desk['p1'][0] = 2
        env.desk['p2'][env.cell_size - 1] = 1
        ball_sum, total_sum = env.ball_sum()
        env.move(env.cell_size)
        self.assertNotEqual(ball_sum, env.ball_sum()[0])
        self.assertEqual(total_sum, env.ball_sum()[1])
        self.assertEqual(1, env.tuzdyk['p2'])





if __name__ == '__main__':
    unittest.main()
