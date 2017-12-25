import numpy as np
import pandas as pd


class T9Desk:

    def __init__(self, p1_id="player_1", p2_id="player_2", cell_size=9):
        # init
        self.p_name = {'p1': p1_id, 'p2': p2_id}
        self.cell_size = cell_size
        self.win_count = {'p1': 0, 'p2': 0, 'draw': 0, 'total': 0}
        # self.game_played_count = 0
        self.observation_space = self.cell_size * 2 + 2
        self.action_space_size = self.cell_size

        # reset
        self.desk = None
        self.move_number = None
        self.who_move = None
        self.score = None
        self.tuzdyk = None
        self.done = None
        self.reset()

        # other
        self.dest_cell = None
        self.action_1to9 = None
        self.total_sum = self.cell_size**2 * 2

    def reset(self, reset_score=False):
        self.desk = {'p1': np.zeros(self.cell_size, dtype=np.int16) + self.cell_size,
                     'p2': np.zeros(self.cell_size, dtype=np.int16) + self.cell_size}
        self.move_number = 0
        self.who_move = False
        self.score = {'p1': 0, 'p2': 0}
        self.tuzdyk = {'p1': -1, 'p2': -2}
        self.done = False
        self.action_1to9 = None
        if reset_score:
            self.win_count = {'p1': 0, 'p2': 0, 'draw': 0, 'total': 0}
        return self.state_symmetric

    @property
    def action_space(self):
        p1_act = []
        p2_act = []
        for i in range(self.cell_size):
            # print(self.desk['p1'][i])
            if (self.desk['p1'][i] != 0) & (i != self.tuzdyk['p2']-1):
                p1_act += [i+1]
            if (self.desk['p2'][i] != 0) & (i != self.tuzdyk['p1']-1):
                p2_act += [i+1]
        return {'p1': np.array(p1_act), 'p2': np.array(p2_act)}

    @property
    def state(self):
        temp = np.append(self.desk['p1'], self.desk['p2'])
        return np.append(temp, np.array([self.score['p1'], self.score['p2']]))

    @property
    def state_symmetric(self):
        pr, op = self.who_moves_str
        temp = np.append(self.desk[pr], self.desk[op])
        return np.append(temp, np.array([self.score[pr], self.score[op]]))

    def _next_state(self, symmetric):
        if symmetric:
            return self.state_symmetric
        else:
            return self.state

    @property
    def state_json(self):
        temp = np.append(self.state, np.array([self.tuzdyk['p1'], self.tuzdyk['p2'], self.who_move]))
        return pd.Series(temp).to_json(orient='values')

    def render(self, do_render=True):
        def star(truth):
            if truth:
                return "*"
            else:
                return " "

        hod = "Move #{}".format(self.move_number)
        if self.move_number != 0:
            if self.who_move:
                hod += "\tp1 from {} to {}".format(self.action_1to9, self.dest_cell)
            else:
                hod += "\tp2 from {} to {}".format(self.action_1to9, self.dest_cell)
        p1 = ""
        p2 = ""
        t1 = list(map(str, self.desk['p1']))
        t2 = list(map(str, self.desk['p2']))
        if self.tuzdyk['p1'] >= 1:
            t2[self.tuzdyk['p1']-1] = "*"
        if self.tuzdyk['p2'] >= 0:
            t1[self.tuzdyk['p2']-1] = "*"
        # print(t1, '\n', t2)
        for i in range(self.cell_size - 1, -1, -1):
            p2 += "{0:3s}".format(t2[i])
        for i in range(self.cell_size):
            p1 += "{0:3s}".format(t1[i])
        p2 += "\t{}{}\tscore: {}\tWin: {}\tDraw: {}".format(self.p_name['p2'], star(self.who_move), self.score['p2'],
                                                            self.win_count['p2'], self.win_count['draw'])
        p1 += "\t{}{}\tscore: {}\tWin: {}\tTotal: {}".format(self.p_name['p1'], star(not self.who_move),
                                                             self.score['p1'], self.win_count['p1'],
                                                             self.win_count['total'])
        ball_sum, total_sum = self.ball_sum
        debug_info = 'sum: {} total_sum: {} Done: {}'.format(ball_sum, total_sum, self.done)
        render = '{}\n{}\n{}\n{}'.format(hod, p2, p1, debug_info)
        if do_render:
            print(render)
        return render

    def step(self, action_1to9, symmetric_state=False):
        self._assert_range_1to9(action_1to9)
        ball_sum, total_sum = self.ball_sum
        pr, op = self.who_moves_str
        score_before = self.score[pr]
        if self.desk[pr][action_1to9-1] > 0:
            # make a move
            self.move(action_1to9)
            # check if game is finished
            self.done = self.check_done
            if self.done:
                # decide who wins
                self.update_win_counter()
            # return info
            score_after = self.score[pr]
            reward = score_after - score_before
            next_state = self._next_state(symmetric_state)
            # switch to another round only after all steps are done
            self.move_number += 1
            self.who_move = ~self.who_move
            self._assert_total_sum(total_sum)
            return next_state, reward, self.done, {'optional': None}
        else:
            reward = -100
            # return info
            next_state = self._next_state(symmetric_state)
            self._assert_total_sum(total_sum)
            return next_state, reward, self.done, {'debug_info': 'empty cell was chosen'}

    def move(self, action_1to9):
        self._assert_range_1to9(action_1to9)
        self.action_1to9 = action_1to9
        self.dest_cell = self.get_dest_cell(action_1to9)
        self.distribute_balls_iterative(action_1to9)
        self.take_balls(self.dest_cell)
        self.set_tuzdyk(self.dest_cell)
        self.take_tuzdyk()

    def distribute_balls_iterative(self, action_1to9):
        # self.assert_range_1to9(action_1to9)
        action_0to8 = action_1to9 - 1
        pr, op = self.who_moves_str
        current_cell_value = self.desk[pr][action_0to8]
        offset = action_0to8 + current_cell_value
        rotation_number = (offset - 1) // self.cell_size
        remainder_9 = offset % self.cell_size
        if (offset > 0) & (remainder_9 == 0):  # bag fix
            # because of -1 in "rotation_number = (offset - 1) // self.cell_size"
            # one rotation is not counted and aim of this fix is to compensate it
            rotation_number += 1
        assert rotation_number >= 0
        for iteration in range(rotation_number + 1):
            # print('iteration: {}, rot_num: {}, remainder_9: {}, remainder_18: {}'.format(iteration, rotation_number,
            #                                                                             remainder_9, remainder_18))

            if iteration == 0:
                if current_cell_value == 1:
                    self.desk[pr][action_0to8] = 0
                    if action_1to9 == self.cell_size:
                        self.desk[op][0] += 1
                    else:
                        self.desk[pr][action_1to9] += 1
                elif current_cell_value == 0:
                    print('Empty cell')
                else:
                    self.desk[pr][action_0to8] = 1
                    self.desk[pr][action_1to9:action_0to8 + current_cell_value] += 1
            elif iteration == rotation_number:
                if rotation_number % 2 == 0:
                    self.desk[pr][0:remainder_9] += 1
                else:
                    self.desk[op][0:remainder_9] += 1
            else:
                if iteration % 2 == 0:
                    self.desk[pr] += 1
                else:
                    self.desk[op] += 1
            # print(self.state)
            # self.render()
        # print(self.state)
        # print('\tnext')

    def take_balls(self, dest_cell_1to9):
        pr, op = self.who_moves_str
        if (dest_cell_1to9 > 0) & (dest_cell_1to9 != self.tuzdyk[pr]):
            if self.desk[op][dest_cell_1to9 - 1] % 2 == 0:
                self.score[pr] += self.desk[op][dest_cell_1to9 - 1]
                self.desk[op][dest_cell_1to9 - 1] = 0

    def set_tuzdyk(self, dest_cell_1to9):
        # self.assert_range_1to9(action_1to9)
        pr, op = self.who_moves_str
        if (self.tuzdyk[pr] < 0) & (dest_cell_1to9 > 0):
            if (self.desk[op][dest_cell_1to9 - 1] == 3) & (dest_cell_1to9 != self.cell_size):
                if (dest_cell_1to9 != self.tuzdyk[op]) & (dest_cell_1to9 != self.tuzdyk[pr]):
                    self.tuzdyk[pr] = dest_cell_1to9

    def take_tuzdyk(self):
        pr, op = self.who_moves_str
        assert self.tuzdyk[pr] < self.cell_size
        assert self.tuzdyk[op] < self.cell_size
        assert self.tuzdyk[pr] != self.tuzdyk[op]
        if self.tuzdyk[pr] > 0:
            self.score[pr] += self.desk[op][self.tuzdyk[pr]-1]
            self.desk[op][self.tuzdyk[pr]-1] = 0
        if self.tuzdyk[op] > 0:
            self.score[op] += self.desk[pr][self.tuzdyk[op]-1]
            self.desk[pr][self.tuzdyk[op]-1] = 0

    def get_dest_cell(self, action_1to9):
        self._assert_range_1to9(action_1to9)
        action_0to8 = action_1to9 - 1
        pr, op = self.who_moves_str
        current_cell_value = self.desk[pr][action_0to8]
        if current_cell_value == 1:
            if action_1to9 == self.cell_size:
                self.dest_cell = 1
            else:
                self.dest_cell = -action_1to9-1
        elif current_cell_value == 0:
            self.dest_cell = - action_1to9
        else:
            temp = (action_0to8 + current_cell_value) % (self.cell_size * 2)
            if temp > self.cell_size:
                self.dest_cell = temp - self.cell_size
            elif temp == 0:
                self.dest_cell = self.cell_size
            else:
                self.dest_cell = -temp
        return self.dest_cell

    @property
    def check_done(self):
        pr, op = self.who_moves_str
        if self.score[pr] > self.cell_size**2:
            return True
        if self.score[op] > self.cell_size**2:
            return True
        if self.desk[op].sum() == 0:
            return True
        return False

    def update_win_counter(self):
        pr, op = self.who_moves_str
        # TODO: add assertions
        if self.score[pr] > self.cell_size ** 2:
            self.win_count[pr] += 1
        elif self.score[op] > self.cell_size ** 2:
            self.win_count[op] += 1
        elif (self.desk[op].sum() == 0) & (self.desk[pr].sum() == 0):
            self.win_count['draw'] += 1
        elif self.desk[op].sum() == 0:
            # self.score[pr] += self.desk[pr].sum()
            self.win_count[pr] += 1
        self.win_count['total'] += 1
        return None

    # additional methods
    @property
    def who_moves_str(self):
        if ~self.who_move:
            pr = 'p1'
            op = 'p2'
        else:
            pr = 'p2'
            op = 'p1'
        return pr, op

    @property
    def ball_sum(self):
        ball_sum = self.desk['p1'].sum() + self.desk['p2'].sum()
        total_sum = self.desk['p1'].sum() + self.desk['p2'].sum() + self.score['p1'] + self.score['p2']
        return ball_sum, total_sum

    def _assert_range_1to9(self, action_1to9):
        try:
            assert action_1to9 >= 1, '1<={}<={}'.format(action_1to9, self.cell_size)
            assert action_1to9 <= self.cell_size, '1<={}<={}'.format(action_1to9, self.cell_size)
        except AssertionError:
            msg = "\033[33m Assertion Error, out of range:\n<env state>\n" \
                  "{}\n</env state>\033[0m".format(self.render(False))
            print(msg)

    def _assert_total_sum(self, total_sum):
        try:
            assert total_sum == self.ball_sum[1]
        except AssertionError:
            msg = "\033[33m Assertion Error, total_sum is inconsistent:\n<env state>\n" \
                  "{}\n</env state>\033[0m".format(self.render(False))
            print(msg)
