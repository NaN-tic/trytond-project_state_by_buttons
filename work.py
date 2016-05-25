# This file is part of the project_state_by_button module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Work']


class Work:
    __metaclass__ = PoolMeta
    __name__ = 'project.work'

    @classmethod
    def __setup__(cls):
        super(Work, cls).__setup__()
        cls.state.readonly = True
        cls._buttons.update({
                'open': {
                    'invisible': Eval('state') == 'opened',
                    },
                'done': {
                    'invisible': Eval('state') == 'done',
                    },
                })

    @classmethod
    @ModelView.button
    def open(cls, works):
        cls.write(works, {'state': 'opened'})

    @classmethod
    @ModelView.button
    def done(cls, works):
        cls.write(works, {'state': 'done'})
