import mock

__all__ = ('ModelMock',)


def ModelMock(model):
    """
    >>> Post = ModelMock(Post)
    >>> assert post.pk == post.id
    """
    class ModelMock(mock.MagicMock):
        def _get_child_mock(self, **kwargs):
            name = kwargs.get('name', '')
            if name == 'pk':
                return self.id
            return super(ModelMock, self)._get_child_mock(**kwargs)
    return ModelMock(spec=model())
