# -*- encoding: utf-8 -*-
################################################################################
#                                                                              #
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol                  #
#                                                                              #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU Affero General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU Affero General Public License for more details.                          #
#                                                                              #
# You should have received a copy of the GNU Affero General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
################################################################################

from openerp.osv import fields, osv

class clv_insurance_client_category(osv.osv):
    _name = 'clv_insurance_client.category'

    def name_get(self, cr, uid, ids, context=None):
        """Return the category's display name, including their direct
           parent by default.

        :param dict context: the ``insurance_client_category_display`` key can be
                             used to select the short version of the
                             category (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if context is None:
            context = {}
        if context.get('insurance_client_category_display') == 'short':
            return super(insurance_client_category, self).name_get(cr, uid, ids, context=context)
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)


    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'name': fields.char('Insurance Client Category', required=True, size=64, translate=True),
        'parent_id': fields.many2one('clv_insurance_client.category', 'Parent Category', select=True, ondelete='restrict'),
        'description': fields.text(string='Description'),
        'notes': fields.text(string='Notes'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Insurance Client Category', store=True),
        'child_ids': fields.one2many('clv_insurance_client.category', 'parent_id', 'Child Categories'),
        'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the category without removing it."),
        'parent_left': fields.integer('Left parent', select=True),
        'parent_right': fields.integer('Right parent', select=True),
        'insurance_client_ids': fields.one2many('clv_insurance_client', 
                                                'category_id', 
                                                'Insurance Client Clients'),
    }
    
    _constraints = [
        (osv.osv._check_recursion, 'Error! You can not create recursive categories.', ['parent_id'])
    ]
    _defaults = {
        'active': 1,
    }
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

class clv_insurance_client(osv.osv):
    _inherit = 'clv_insurance_client'

    _columns = {
        'category_id': fields.many2one('clv_insurance_client.category', 'Category'),
    }
