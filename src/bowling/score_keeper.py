class ScoreKeeper:
    """
    Handles the scoring system for the bowling game.

    :ivar scores: The list of individual scores for each throw. Contains `None` for incomplete scores.
    :ivar frame_starts: Set of indices marking the start of each frame within the scores list.
    :ivar frame_throws: List containing sublists, where each one represents the throws of a single frame.
    """

    def __init__(self) -> None:
        """
        Initialises the scorekeeper object.
        """
        self.scores: list[int | None] = []
        self.frame_starts: set[int] = set()
        self.frame_throws: list[list[int]] = []

    @property
    def finished(self) -> bool:
        """
        Indicates whether the game has finished by checking if the number of frames
        is equal to 10 (the standard number of frames in a bowling game).

        :return: True if the number of frames is equal to 10, otherwise False.
        """
        return len(self.frames) == 10

    @property
    def is_last_frame(self):
        """
        Checks if the current frame will be the last frame of the game by checking if
        the number of frames is equal to 9 (the standard number of frames in a bowling
        game - 1).

        :return: True if the number of frames is equal to 9, otherwise False.
        """
        return len(self.frames) == 9

    @property
    def valid_scores(self) -> list[int]:
        """
        Returns the scores list but with any None values filtered out and not included.

        :returns: A list containing all scores from self.scores that are not None.
        """
        return [score for score in self.scores if score is not None]

    @property
    def total_score(self) -> int:
        """
        Returns the total score of the game by summing the list of valid scores.

        :return: The sum of self.valid_scores.
        """
        return sum(self.valid_scores)

    @property
    def frames(self) -> list[list[int]]:
        """

        Returns the list of frames, by slicing the scores list, by the starting
        positions of each frame defined in the frame_starts list.

        :return: A list containing sublists, with each sublist representing a frame.
        """
        result = []
        sorted_frame_starts = sorted(self.frame_starts)
        prev_frame_start = sorted_frame_starts[0]
        for frame_start in sorted_frame_starts[1:]:
            result.append(self.scores[prev_frame_start:frame_start])
            prev_frame_start = frame_start
        result.append(self.scores[prev_frame_start:])
        return result

    @property
    def frame_scores(self) -> list[int | None]:
        """
        Calculates the total score for each frame. If a frame contains any None values
        (indicating that it is incomplete), the corresponding score will also have a
        value of None. Otherwise, the sum of the frame's scores will be calculated.

        :return: A list containing the total scores (or None values) for each frame.
        """
        return [sum([score for score in frame]) if None not in frame else None for frame in self.frames]

    def __str__(self) -> str:
        """
        Returns a string representation of the object, detailing for each frame,
        the throws made in it and its current cumulative score.

        :return: A formatted string displaying the details for each frame.
        """
        result = "\n"
        c_score = 0
        for i, frame in enumerate(self.frames):
            c_frame_score = self.frame_scores[i]
            if c_frame_score is not None and c_score != -1:
                c_score += c_frame_score
                result += f"Frame {i + 1}:\n{self.frame_throws[i]} {c_score}\n"
            else:
                c_score = -1
                result += f"Frame {i + 1}:\n{self.frame_throws[i]} Uncalculated\n"
        return result

    def end_frame(self, frame: list[int]) -> None:
        """
        Ends the provided frame by adding the frame's start index to the frame_starts list,
        determining its type (strike, spare or open), running the correct method to end it,
        and adds the frame to the frame_throws list.

        :param frame: The list of integers representing the scores for each throw in a frame.
        """
        frame_start = len(self.scores)
        self.frame_starts.add(frame_start)
        if len(self.frame_starts) == 10:
            self.end_last_frame(frame)
        elif frame == [10]:
            self.end_strike_frame()
        elif sum(frame) == 10:
            self.end_spare_frame(frame)
        else:
            self.end_open_frame(frame)
        self.frame_throws.append(frame)

    def end_open_frame(self, frame: list[int]) -> None:
        """
        Ends the provided open frame calculating any uncalculated scores from previous strikes and
        spares, and saving the frame's scores to the scores list.

        :param frame: The list of integers representing the scores for each throw in a frame.
        """
        self.calc_strikes_and_spares(frame)
        self.scores.extend(frame)

    def end_spare_frame(self, frame: list[int]) -> None:
        """
        Ends the provided spare frame, calculating any uncalculated scores from previous strikes and
        spares, and saving the frame's scores, alongside an extra None value to account for the next
        throw, to the scores list.

        :param frame: The list of integers representing the scores for each throw in a frame.
        """
        self.calc_strikes_and_spares(frame)
        self.scores.extend([*frame, None])

    def end_strike_frame(self) -> None:
        """
        Ends a strike frame, calculating any uncalculated scores from previous strikes and spares, and
        saving a single 10 score, alongside two extra None values to account for the next
        two throws, to the scores list.
        """
        self.calc_strikes_and_spares([10])
        self.scores.extend([10, None, None])

    def end_last_frame(self, frame: list[int]) -> None:
        """
        Ends the last frame, calculating the appropriate scores depending on the outcome of the
        frame's throws (strike/spare/open). Ensures that the total scores for each frame don't
        exceed the maximum of 30 points.

        :param frame: The list of integers representing the scores for each throw in a frame.
        """
        # If the first throw is a strike
        if frame[0] == 10:
            self.end_strike_frame()
        else:  # The first throw isn't a strike
            if sum(frame[0:2]) == 10:  # The first two throws sum to a spare
                self.end_spare_frame(frame)
                self.end_open_frame([frame[-1], 0])  # Add the third throw to the frame
                return
            else:  # The two throws leave an open frame
                self.end_open_frame(frame)
        # If the first AND second throws are strikes
        if frame[1] == 10:
            self.end_strike_frame()
        else:  # Only the first throw was a strike
            self.end_open_frame(frame)
            return
        # Add the third throw to the frame
        self.end_open_frame([frame[-1], 0])
        # Adjust each frame to make sure they don't exceed the limit of 30
        for frame in self.frames:
            frame_total = sum(frame)
            if sum(frame) > 30:
                self.scores.append(30 - frame_total)

    def calc_strikes_and_spares(self, frame: list[int]) -> None:
        """
        Calculates and updates any uncalculated scores from strikes and spares, using the
        current frame. If the frame list does not supply enough values, it uses the value
        of the last non-None score to fill the missing scores.

        :param frame: The list of integers representing the scores for each throw in a frame.
        """
        frame = frame.copy()
        while None in self.scores:
            n_index = len(self.scores) - 1 - self.scores[::-1].index(None)
            if frame:
                self.scores[n_index] = frame.pop()
            else:
                # TODO: Check that this logic is correct with more examples
                # print(self.scores[-2])
                self.scores[n_index] = self.scores[-2]
                break
        # print(self.scores)


# Example game - https://bowlingforbeginners.com/how-is-bowling-scored/
if __name__ == '__main__':
    sk = ScoreKeeper()
    sk.end_frame([6, 2])
    sk.end_frame([10])
    sk.end_frame([3, 2])
    sk.end_frame([5, 5])
    sk.end_frame([10])
    sk.end_frame([10])
    sk.end_frame([1, 4])
    sk.end_frame([9, 0])
    sk.end_frame([3, 2])
    sk.end_frame([10, 10, 10])
    # print(sk.scores, sk.total_score)
    # print(sk.frame_starts)
    # print(sk.frames)
    print(sk)
