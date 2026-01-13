import json
import os
from typing import List, Dict, Any

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
    
    klimatprof_products = [
        {
            'id': 'kp_1',
            'name': 'Fujitsu ASYG09KMCC/AOYG09KMCC',
            'brand': 'Fujitsu',
            'category': 'Инверторные сплит-системы',
            'series': 'Genios',
            'power': 2.5,
            'type': 'Настенный',
            'price': 49900,
            'source': 'klimatprof.online',
            'image': 'https://images.unsplash.com/photo-1585909695284-32d2985ac9c0?w=400&h=300&fit=crop',
            'features': ['Инвертор', 'Wi-Fi управление', 'Очистка воздуха']
        },
        {
            'id': 'kp_2',
            'name': 'Lessar LS-H09KLA2A/LU-H09KLA2A',
            'brand': 'Lessar',
            'category': 'Инверторные сплит-системы',
            'series': 'Stella',
            'power': 2.6,
            'type': 'Настенный',
            'price': 32900,
            'source': 'klimatprof.online',
            'image': 'https://images.unsplash.com/photo-1631545805119-17cbd88d3d53?w=400&h=300&fit=crop',
            'features': ['Инвертор', 'Низкий уровень шума', 'Режим сна']
        },
        {
            'id': 'kp_3',
            'name': 'TOSOT T09H-SLyR/I/T09H-SLyR/O',
            'brand': 'TOSOT',
            'category': 'Инверторные сплит-системы',
            'series': 'Lyra',
            'power': 2.6,
            'type': 'Настенный',
            'price': 38900,
            'source': 'klimatprof.online',
            'image': 'https://images.unsplash.com/photo-1634641283431-5c644bb6f944?w=400&h=300&fit=crop',
            'features': ['Инвертор', 'Самоочистка', 'LED дисплей']
        },
        {
            'id': 'kp_4',
            'name': 'Quattroclima QV-LO09WAE/QN-LO09WAE',
            'brand': 'Quattroclima',
            'category': 'Инверторные сплит-системы',
            'series': 'Lanterna',
            'power': 2.5,
            'type': 'Настенный',
            'price': 29900,
            'source': 'klimatprof.online',
            'image': 'https://images.unsplash.com/photo-1585909695284-32d2985ac9c0?w=400&h=300&fit=crop',
            'features': ['Инвертор', 'Турбо режим', 'Таймер 24ч']
        }
    ]
    
    breez_products = [
        {
            'id': 'br_1',
            'name': 'Hisense AS-09HR4SYDDC15',
            'brand': 'Hisense',
            'category': 'Кондиционеры',
            'series': 'Smart DC Inverter',
            'power': 2.6,
            'type': 'Настенный',
            'price': 44900,
            'source': 'breez.ru',
            'image': 'https://images.unsplash.com/photo-1631545805119-17cbd88d3d53?w=400&h=300&fit=crop',
            'features': ['Инвертор', 'Wi-Fi', 'Самодиагностика']
        },
        {
            'id': 'br_2',
            'name': 'Royal Clima RC-V29HN',
            'brand': 'Royal Clima',
            'category': 'Кондиционеры',
            'series': 'Vela',
            'power': 2.7,
            'type': 'Настенный',
            'price': 36900,
            'source': 'breez.ru',
            'image': 'https://images.unsplash.com/photo-1634641283431-5c644bb6f944?w=400&h=300&fit=crop',
            'features': ['Инвертор', 'Антибактериальный фильтр', 'Авторестарт']
        },
        {
            'id': 'br_3',
            'name': 'Funai RACI-SN25HP.D03',
            'brand': 'Funai',
            'category': 'Кондиционеры',
            'series': 'Sensei',
            'power': 2.5,
            'type': 'Настенный',
            'price': 41900,
            'source': 'breez.ru',
            'image': 'https://images.unsplash.com/photo-1585909695284-32d2985ac9c0?w=400&h=300&fit=crop',
            'features': ['Инвертор', 'Плазменный фильтр', 'I Feel функция']
        },
        {
            'id': 'br_4',
            'name': 'Zilon ZT-09IS',
            'brand': 'Zilon',
            'category': 'Кондиционеры',
            'series': 'Inverter',
            'power': 2.6,
            'type': 'Настенный',
            'price': 33900,
            'source': 'breez.ru',
            'image': 'https://images.unsplash.com/photo-1631545805119-17cbd88d3d53?w=400&h=300&fit=crop',
            'features': ['Инвертор', 'Ночной режим', 'Холод/Тепло']
        },
        {
            'id': 'br_5',
            'name': 'Hitachi RAK-18RPD/RAC-18WPD',
            'brand': 'Hitachi',
            'category': 'Кондиционеры',
            'series': 'Performance',
            'power': 5.0,
            'type': 'Настенный',
            'price': 67900,
            'source': 'breez.ru',
            'image': 'https://images.unsplash.com/photo-1634641283431-5c644bb6f944?w=400&h=300&fit=crop',
            'features': ['Инвертор', 'Мощная система', '3D воздушный поток']
        }
    ]
    
    products.extend(klimatprof_products)
    products.extend(breez_products)
    
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
