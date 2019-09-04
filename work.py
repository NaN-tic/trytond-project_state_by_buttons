# This file is part of the project_state_by_button module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction

__all__ = ['Work']


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'
    active = fields.Function(fields.Boolean('Active'), 'get_active',
        searcher='search_active')

    @classmethod
    def __setup__(cls):
        super(Work, cls).__setup__()
        cls.state.readonly = True
        cls._buttons.update({
                'open': {
                    'invisible': Eval('state') != 'done',
                    },
                'done': {
                    'invisible': Eval('state') != 'opened',
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

    @classmethod
    def get_total(cls, works, names):
        with Transaction().set_context(active_test=False):
            return super().get_total(works, names)

    def get_active(self, name):
        if self.type == 'project':
            return self.state == 'opened'
        return True

    @classmethod
    def search_active(cls, name, clause):
        operator = clause[1] == '=' and 1 or -1
        operand = clause[2] and 1 or -1
        sign = operator * operand

        if sign > 0:
            return ['OR', [
                    ('type', '=', 'task')
                    ], [
                    ('type', '=', 'project'),
                    ('state', '=', 'opened'),
                    ]
                ]
        else:
            return [
                ('type', '=', 'project'),
                ('state', '=', 'done'),
                ]
