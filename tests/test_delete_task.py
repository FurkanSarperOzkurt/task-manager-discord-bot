import database


def test_delete_task(test_db):
    """gorev ekle sonra sil, calisiyormu bak"""
    tid = database.add_task("silinecek gorev", test_db)
    result = database.delete_task(tid, test_db)

    assert result is True
    tasks = database.get_tasks(test_db)
    assert len(tasks) == 0


def test_delete_nonexistent(test_db):
    """olmayan gorevi silmeye calisinca False donmeli"""
    result = database.delete_task(999, test_db)
    assert result is False


def test_delete_only_target(test_db):
    """birden fazla gorev varken sadece istedigimi silmeli"""
    t1 = database.add_task("kalacak", test_db)
    t2 = database.add_task("silinecek", test_db)

    database.delete_task(t2, test_db)
    tasks = database.get_tasks(test_db)

    assert len(tasks) == 1
    assert tasks[0]["description"] == "kalacak"


def test_delete_twice(test_db):
    """ayni gorevi iki kez silersem ikincisi False olmali"""
    tid = database.add_task("test", test_db)
    first = database.delete_task(tid, test_db)
    second = database.delete_task(tid, test_db)

    assert first is True
    assert second is False