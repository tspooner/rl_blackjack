def to_state(hand, upcard):
    return (hand.value()-12, int(upcard)-1, int(hand.usable_ace))
