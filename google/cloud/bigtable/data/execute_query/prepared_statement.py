# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Dict, Optional

from google.cloud.bigtable.data.execute_query.metadata import (
    Metadata,
    SqlType,
    _pb_metadata_to_metadata_types,
)
from google.cloud.bigtable_v2.types.bigtable import (
    PrepareQueryRequest,
    PrepareQueryResponse,
)


class _PrepareResponse:
    """
    Parsed representation of a proto ``PrepareQueryResponse``. Use this so
    we only need to parse metadata once, instead of per ``ExecuteQuery`` request.

    Intended for internal use only.
    """

    def __init__(self, proto_response: PrepareQueryResponse):
        self._proto = proto_response
        self.__metadata = _pb_metadata_to_metadata_types(proto_response.metadata)

    def _prepared_query(self) -> bytes:
        return self._proto.prepared_query

    def _metadata(self) -> Metadata:
        return self.__metadata


class PreparedStatement(object):
    """
    Represents a cached query plan that can be run using `execute_query`.

    All methods are intended for internal use only. The only intended use
    for users is via execute_query.å
    """

    def __init__(
        self,
        instance_id: str,
        prepare_query_response: PrepareQueryResponse,
        param_types: Dict[str, SqlType.Type],
        prepare_query_request: PrepareQueryRequest,
    ):
        self.__instance_id = instance_id
        self.__prepare_response = _PrepareResponse(prepare_query_response)
        self.__param_types = param_types
        self.__prepare_query_request = prepare_query_request

    def _prepare_query_response(self) -> _PrepareResponse:
        return self.__prepare_response

    def _param_types(self) -> Dict[str, SqlType.Type]:
        return self.__param_types

    def _instance_id(self) -> str:
        return self.__instance_id

    def _instance_name(self) -> str:
        return self.__prepare_query_request.instance_name

    def _app_profile_id(self) -> Optional[str]:
        return self.__prepare_query_request.app_profile_id
