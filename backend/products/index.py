import json
import os
from typing import List, Dict, Any
from parsers import parse_klimatprof, parse_breez

def handler(event: dict, context) -> dict:
    '''
    API для получения данных о климатическом оборудовании
    Объединяет информацию с klimatprof.online и breez.ru
    '''
    method = event.get('httpMethod', 'GET')

    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': '',
            'isBase64Encoded': False
        }

    if method == 'GET':
        try:
            products = get_all_products()
            
            query_params = event.get('queryStringParameters', {}) or {}
            min_price = query_params.get('min_price')
            max_price = query_params.get('max_price')
            brand = query_params.get('brand')
            product_type = query_params.get('type')

            filtered_products = filter_products(
                products, 
                min_price=min_price,
                max_price=max_price,
                brand=brand,
                product_type=product_type
            )

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'products': filtered_products,
                    'total': len(filtered_products),
                    'sources': ['klimatprof.online', 'breez.ru']
                }, ensure_ascii=False),
                'isBase64Encoded': False
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': str(e)}, ensure_ascii=False),
                'isBase64Encoded': False
            }

    return {
        'statusCode': 405,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': 'Method not allowed'}, ensure_ascii=False),
        'isBase64Encoded': False
    }


def get_all_products() -> List[Dict[str, Any]]:
    '''Получает все товары из обоих источников'''
    products = []
    
    try:
        klimatprof_products = parse_klimatprof()
        products.extend(klimatprof_products)
    except Exception as e:
        print(f'Error parsing klimatprof: {e}')
    
    try:
        breez_products = parse_breez()
        products.extend(breez_products)
    except Exception as e:
        print(f'Error parsing breez: {e}')
    
    return products


def filter_products(
    products: List[Dict[str, Any]], 
    min_price: str = None,
    max_price: str = None,
    brand: str = None,
    product_type: str = None
) -> List[Dict[str, Any]]:
    '''Фильтрует товары по заданным параметрам'''
    filtered = products
    
    if min_price:
        try:
            min_p = float(min_price)
            filtered = [p for p in filtered if p['price'] >= min_p]
        except ValueError:
            pass
    
    if max_price:
        try:
            max_p = float(max_price)
            filtered = [p for p in filtered if p['price'] <= max_p]
        except ValueError:
            pass
    
    if brand:
        filtered = [p for p in filtered if p['brand'].lower() == brand.lower()]
    
    if product_type:
        filtered = [p for p in filtered if p['type'].lower() == product_type.lower()]
    
    return filtered