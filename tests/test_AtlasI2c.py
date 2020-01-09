from AtlasI2C import AtlasI2C


class TestAtlasI2C:
    def test_init(self):
        dev = AtlasI2C()
        assert isinstance(dev, AtlasI2C)
