STATUS_OK = {
    "CREATE": "ROUTINE_CREATE_OK",
    "LIST": "ROUTINE_LIST_OK",
    "DETAIL": "ROUTINE_DETAIL_OK",
    "UPDATE": "ROUTINE_UPDATE_OK",
    "DELETE": "ROUTINE_DELETE_OK",
    "RESULT_UPDATE": "RESULT_UPDATE_OK"
}

STATUS_FAIL = {
    "CREATE": "ROUTINE_CREATE_FAIL",
    "LIST": "ROUTINE_LIST_FAIL",
    "DETAIL": "ROUTINE_DETAIL_FAIL",
    "UPDATE": "ROUTINE_UPDATE_FAIL",
    "DELETE": "ROUTINE_DELETE_FAIL",
    "RESULT_UPDATE": "RESULT_UPDATE_FAIL"
}

API_MESSAGE_OK = {
    "CREATE": "Routine이 생성되었습니다.",
    "UPDATE": "Routine이 수정되었습니다.", 
    "DELETE": "Routine이 삭제되었습니다.",
    "DETAIL": "Routine 조회 성공",
    "LIST": "Routine 리스트 조회 성공",
    "RESULT_UPDATE": "Result 업데이트 성공"
}

API_MESSAGE_FAIL = {
    "CREATE": "Routine 생성이 실패하였습니다.",
    "DELETE": "Routine 삭제가 실패하였습니다.",

    "DETAIL": "Routine 조회 실패",
    "LIST": "Routine 리스트 조회 실패",
    "RESULT_UPDATE": "Result 업데이트 실패"
}
