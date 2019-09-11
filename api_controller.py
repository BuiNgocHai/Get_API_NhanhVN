from odoo import http, _
from odoo.http import request
from odoo.addons.lc_rest_api.controllers.controllers import validate_token, generate_response, getRequestIP, serialization_data, toUserDatetime, _args, permission_check

class ApiGetData(http.Controller):
    #Tinh phi cho mot don hang
    @validate_token
    @http.route(['/api/shipping/fee/', '/api/shipping/fee/<delivery_price>'], methods=['GET'], type='http', auth='none', csrf=False)
    def model_delivery_price_config(self, access_token, delivery_price=None, **kw):
        if not permission_check('sale.order', 'read'):
            return generate_response(data={
                'success': False,
                'msg': "Create permission denied"
            })
        if not delivery_price:
            try:
                _domain, _fields, _offset, _limit, _order = _args(kw)
                data = request.env['sale.order'].search_read(fields=['id', 'name', 'delivery_price','carrier_id','expected_date','partner_invoice_id'], offset=_offset, limit=_limit, order=_order)
                data2 = request.env['delivery.carrier'].search_read(fields=['id', 'name','website_description'], offset=_offset, limit=_limit, order=_order)
                #dia chi giao hang
                data3 = request.env['res.partner'].search_read(fields=['id', 'city','state_id','name'], offset=_offset, limit=_limit, order=_order) 
                #dia chi kho
                data5 = request.env['sale.order'].search_read(fields=['id','warehouse_id','create_uid_interger' ], offset=_offset, limit=_limit, order=_order)
                new_data = []
                for i in range(len(data)):    
                    if data[i]['carrier_id'] == False:
                        data[i]['carrier_id'] = 0
                        new_list ={
                            'id': data[i]['id'],
                            'name': data[i]['name'],
                            'carrier_id': 0,
                            'carrier_name': False,
                            'serviceDescription': False,
                            'estimatedDeliveryTime': data[i]['expected_date'],
                            'shipFee': data[i]['delivery_price']
                            
                        }
                        new_data.append(new_list)
                    else:
                        serviceDescription = ''
                        for delivery_name in range(len(data2)):
                            if data[i]['carrier_id'][1] == data2[delivery_name]['name']:
                                serviceDescription = data2[delivery_name]['website_description']
                                break
                        new_list ={
                            'id': data[i]['id'],
                            'name': data[i]['name'],
                            'carrier_id': data[i]['carrier_id'][0],
                            'carrier_name': data[i]['carrier_id'][1],
                            'serviceDescription': serviceDescription,
                            'estimatedDeliveryTime': data[i]['expected_date'],
                            'shipFee': data[i]['delivery_price']
                            
                        }
                        new_data.append(new_list)
                        
                return generate_response(data={
                    'success': True,
                    'msg': "success",
                    'totalPages': (int)(len(data)/_limit)+1,
                    'page': (int)(_offset/_limit)+1,
                    'data': serialization_data(new_data),
                    'data_count': len(data)
                })
            except Exception as e:
                return generate_response(data={
                    'success': False,
                    'msg': "{}".format(e)
                })
        else:
            try:
                _domain, _fields, _offset, _limit, _order = _args(kw)
                delivery_price = str(delivery_price)
                #tim theo khack hang
                data3 = request.env['res.partner'].search_read(fields=['id', 'city','state_id','name'],domain=[('city', '=', delivery_price)])
                #tim theo kho hang
                data = request.env['sale.order'].search_read(fields=['id', 'name', 'delivery_price','carrier_id','expected_date','partner_shipping_id','partner_invoice_id'], offset=_offset, limit=_limit, order=_order)
                new_data = []
                data2 = request.env['delivery.carrier'].search_read(fields=['id', 'name','website_description'], offset=_offset, limit=_limit, order=_order)
                new_data2 = []
                if len(data3) != 0:
                    for i in range(len(data)):
                        for k in range(len(data3)):
                            if (data[i]['partner_shipping_id'][1] == data3[k]['name']) and (data3[k]['name']!=False):
                                new_data2.append(data[i])
                    if new_data2 == []:
                        for i in range(len(data)):
                            for k in range(len(data3)):
                                if(data[i]['partner_invoice_id'][1] == data3[k]['name']) and (data3[k]['name'] !=False):
                                    new_data2.append(data[i])

                data = new_data2
                for i in range(len(data)):    
                    if data[i]['carrier_id'] == False:
                        data[i]['carrier_id'] = 0
                        new_list ={
                            'id': data[i]['id'],
                            'name': data[i]['name'],
                            'carrier_id': 0,
                            'carrier_name': False,
                            'serviceDescription': False,
                            'estimatedDeliveryTime': data[i]['expected_date'],
                            'shipFee': data[i]['delivery_price']
                            
                        }
                        new_data.append(new_list)
                    else:
                        serviceDescription = ''
                        for delivery_name in range(len(data2)):
                            if data[i]['carrier_id'][1] == data2[delivery_name]['name']:
                                serviceDescription = data2[delivery_name]['website_description']
                                break
                        new_list ={
                            'id': data[i]['id'],
                            'name': data[i]['name'],
                            'carrier_id': data[i]['carrier_id'][0],
                            'carrier_name': data[i]['carrier_id'][1],
                            'serviceDescription': serviceDescription,
                            'estimatedDeliveryTime': data[i]['expected_date'],
                            'shipFee': data[i]['delivery_price']                            
                        }
                        new_data.append(new_list)
                return generate_response(data={
                    'success': True,
                    'msg': "success",
                    'data': serialization_data(new_data, restrict=['customer_facing_display_html', 'session_ids'])
                })
            except Exception as e:
                return generate_response(data={
                    'success': False,
                    'msg': "{}".format(e)
                })

