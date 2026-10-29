from src.logic.coin_logic import flip_coin, CoinStats, CoinSide


def test_flip_coin_defaults():
    res = flip_coin()
    assert res.side in (CoinSide.HEADS, CoinSide.TAILS)
    assert res.label in ("Heads", "Tails")


def test_flip_coin_custom_labels():
    res = flip_coin(heads_label="Pizza", tails_label="Burger")
    assert res.label in ("Pizza", "Burger")


def test_coin_stats():
    stats = CoinStats()
    res1 = flip_coin()
    stats.record(res1)
    assert stats.total_flips == 1
    assert stats.heads_count + stats.tails_count == 1
    assert len(stats.history) == 1

    stats.reset()
    assert stats.total_flips == 0
    assert len(stats.history) == 0
