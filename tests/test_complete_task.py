import database


def test_complete_task(test_db):
    """gorevi tamamla, completed 1 olmali"""
    tid = database.add_task("bitir bunu", test_db)
    result = database.complete_task(tid, test_db)

    assert result is True
    task = database.get_task(tid, test_db)
    assert task["completed"] == 1


def test_complete_nonexistent(test_db):
    """olmayan gorevi tamamlamak False donmeli"""
    result = database.complete_task(999, test_db)
    assert result is False


def test_complete_twice(test_db):
    """zaten bitmis gorevi tekrar tamamlamak sorun olmamali"""
    tid = database.add_task("test gorev", test_db)
    database.complete_task(tid, test_db)
    result = database.complete_task(tid, test_db)

    assert result is True
    task = database.get_task(tid, test_db)
    assert task["completed"] == 1


def test_complete_doesnt_touch_others(test_db):
    """birini tamamlayinca diger gorevler etkilenmemeli"""
    t1 = database.add_task("A gorevi", test_db)
    t2 = database.add_task("B gorevi", test_db)

    database.complete_task(t1, test_db)

    task_a = database.get_task(t1, test_db)
    task_b = database.get_task(t2, test_db)
    assert task_a["completed"] == 1
    assert task_b["completed"] == 0