from __future__ import annotations

import pathlib
from dataclasses import dataclass
from typing import List

import pandas as pd
from aenum import Enum, auto
from shapely.geometry import Point


class TrajectoryUnit(Enum):
    """Identifier of the unit of the trajectory coordinates"""

    _init_ = "value __doc__"
    METER = 1, "meter (m)"
    CENTIMETER = 100, "centimeter (cm)"


class TrajectoryType(Enum):
    """Identifier for the type of trajectory"""

    _init_ = "value __doc__"

    PETRACK = auto(), "PeTrack trajectory"
    JUPEDSIM = auto(), "JuPedSim trajectory"
    FALLBACK = auto(), "trajectory of unknown type"


@dataclass(frozen=True)
class TrajectoryData:
    """Trajectory Data

    Wrapper around the trajectory data, holds the data as a data frame.

    Note:
        The coordinate data is stored in meter ('m')!

    Attributes:
        _data (pd.DataFrame): data frame containing the actual data in the form:
            "ID", "frame", "X", "Y", "Z"

        frame_rate (float): frame rate of the trajectory file

        trajectory_type (TrajectoryType): type of the trajectory used

        file (pothlib.Path): file from which is trajectories was read

    """

    _data: pd.DataFrame
    frame_rate: float
    trajectory_type: TrajectoryType
    file: pathlib.Path

    def get_pedestrian_positions(self, frame: int, pedestrian_id: int, window: int) -> List[Point]:
        """Return the pedestrian position within a given frame window.

        The frame window ([min_frame, max_frame]) is determined by frame and the window:
        min_frame = frame - window/2 if that is included in the trajectory else frame
        max_frame = frame + window/2 if that is included in the trajectory else frame

        Args:
            frame (int): reference frame
            pedestrian_id (int): id of the pedestrian
            window (int): window size

        Returns:
            All positions of the pedestrian with the given ID within [min_frame, max_frame]
        """
        window /= 2
        pedestrian_positions = self._data.loc[self._data["ID"] == pedestrian_id][
            ["ID", "frame", "X", "Y"]
        ].sort_values(by=["frame"])

        min_frame = (
            frame - window if pedestrian_positions["frame"].min() <= frame - window else frame
        )
        max_frame = (
            frame + window if pedestrian_positions["frame"].max() >= frame + window else frame
        )

        pedestrian_positions_frame_window = pedestrian_positions.loc[
            (pedestrian_positions["frame"] >= min_frame)
            & (pedestrian_positions["frame"] <= max_frame)
        ][["frame", "X", "Y"]].sort_values(by=["frame"])

        return [
            Point(row["X"], row["Y"]) for _, row in pedestrian_positions_frame_window.iterrows()
        ]

    def get_min_frame(self) -> int:
        """Returns first frame for which data a position is recorded"""
        return self._data["frame"].min()

    def get_max_frame(self) -> int:
        """Returns last frame for which data a position is recorded"""
        return self._data["frame"].max()

    def get_positions(self, frame):
        """Return the position of all pedestrians in a specific frame

        Args:
            frame (int): frame for which the positions are returned

        Returns:
            Dict from pedestrian id to Point(x,y) in frame
        """
        positions = self._data.loc[self._data["frame"] == frame][["ID", "X", "Y"]]
        positions = positions.set_index("ID")
        return {
            agent_id: Point(position["X"], position["Y"])
            for agent_id, position in positions.to_dict("index").items()
        }

    def get_time_in_s(self, frame: int) -> float:
        """Returns the time in seconds for a specific frame (frame 0 is at 0 s)"""
        return frame / self.frame_rate
