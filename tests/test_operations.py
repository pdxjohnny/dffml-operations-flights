import sys
import pathlib
import contextlib
import urllib.parse
from typing import NamedTuple, List

import bs4
import aiohttp

from dffml import opimp_in, op, Input, DataFlow, run, GetSingle, AsyncTestCase

from dffml_operations_flights import *


OPIMPS = opimp_in(sys.modules[__name__])


class TestOperations(AsyncTestCase):
    async def test_run(self):
        dataflow = DataFlow.auto(*OPIMPS)
        check = {
            "PDX to HNL depart 9/2/21 return 9/6/21 for 2 adults": (
                (
                    ("Portland, OR (PDX-Portland Intl.)", "src"),
                    ("Honolulu, HI (HNL-Honolulu Intl.)", "dst"),
                    ("9/2/21", "leave"),
                    ("9/6/21", "back"),
                    (2, "adults"),
                ),
                {},
            )
        }
        async for ctx, results in run(
            dataflow,
            {
                ctx_str: [
                    Input(
                        value=value,
                        definition=dataflow.definitions[
                            "alaskaair_round_trip_html.inputs." + definition
                        ],
                    )
                    for value, definition in inputs
                ]
                for ctx_str, (inputs, _results) in check.items()
            },
        ):
            ctx_str = (await ctx.handle()).as_string()
            self.assertDictEqual(check[ctx_str][1], results)
