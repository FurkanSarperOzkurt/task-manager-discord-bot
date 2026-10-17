import database


def test_show_empty(test_db):
    """hic gorev yokken bos liste gelmeli"""
    tasks = database.get_tasks(test_db)
    assert len(tasks) == 0


def test_show_multiple(test_db):
    """birden fazla gorev listelenebilmeli"""
    database.add_task("Task 1", test_db)
    database.add_task("Task 2", test_db)

    tasks = database.get_tasks(test_db)
    assert len(tasks) == 2
    assert tasks[0]["description"] == "Task 1"
    assert tasks[1]["description"] == "Task 2"


def test_show_with_completed(test_db):
    """tamamlanmis gorev status'u dogru gosterilmeli"""
    database.add_task("bitmedi", test_db)
    tid = database.add_task("bitti", test_db)
    database.complete_task(tid, test_db)

    tasks = database.get_tasks(test_db)
    assert tasks[0]["completed"] == 0
    assert tasks[1]["completed"] == 1


def test_get_single_task(test_db):
    """tek gorev getirmek calismali"""
    tid = database.add_task("tek gorev", test_db)
    task = database.get_task(tid, test_db)
    assert task is not None
    assert task["description"] == "tek gorev"


def test_get_nonexistent(test_db):
    """olmayan gorev None donmeli"""
    task = database.get_task(9999, test_db)
    assert task is None