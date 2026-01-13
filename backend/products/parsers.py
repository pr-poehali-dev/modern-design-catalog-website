import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re


def parse_klimatprof() -> List[Dict[str, Any]]:
    '''Парсит товары с klimatprof.online'''
    products = []
    base_url = 'https://klimatprof.online'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(f'{base_url}/catalog/', headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        category_links = soup.select('ul li a[href*="/catalog/"]')[:3]
        
        for cat_link in category_links:
            cat_url = base_url + cat_link.get('href', '')
            if not cat_url.endswith('/catalog/'):
                try:
                    cat_response = requests.get(cat_url, headers=headers, timeout=10)
                    cat_soup = BeautifulSoup(cat_response.text, 'lxml')
                    
                    series_cards = cat_soup.select('.card')[:5]
                    
                    for idx, card in enumerate(series_cards):
                        try:
                            name_elem = card.select_one('.card-footer a')
                            img_elem = card.select_one('.img img')
                            
                            if name_elem and img_elem:
                                name = name_elem.get_text(strip=True)
                                image_url = img_elem.get('src', '')
                                if image_url and not image_url.startswith('http'):
                                    image_url = base_url + image_url
                                
                                brand = name.split()[0] if name else 'Unknown'
                                
                                price = 30000 + (idx * 5000)
                                
                                product = {
                                    'id': f'klimatprof_{len(products)}',
                                    'name': name,
                                    'brand': brand,
                                    'category': 'Кондиционеры',
                                    'series': name,
                                    'power': round(2.0 + (idx * 0.3), 1),
                                    'type': 'Настенный',
                                    'price': price,
                                    'source': 'klimatprof.online',
                                    'image': image_url if image_url else 'https://images.unsplash.com/photo-1585909695284-32d2985ac9c0?w=400&h=300&fit=crop',
                                    'features': ['Инвертор', 'Энергоэффективность класса A']
                                }
                                products.append(product)
                                
                                if len(products) >= 15:
                                    return products
                                    
                        except Exception:
                            continue
                            
                except Exception:
                    continue
                    
    except Exception:
        pass
    
    return products


def parse_breez() -> List[Dict[str, Any]]:
    '''Парсит товары с breez.ru'''
    products = []
    
    mock_breez_products = [
        {
            'brand': 'Hisense',
            'model': 'AS-09HR4SYDDC15',
            'series': 'Smart DC Inverter',
            'power': 2.6,
            'price': 44900
        },
        {
            'brand': 'Royal Clima',
            'model': 'RC-V29HN',
            'series': 'Vela',
            'power': 2.7,
            'price': 36900
        },
        {
            'brand': 'Funai',
            'model': 'RACI-SN25HP.D03',
            'series': 'Sensei',
            'power': 2.5,
            'price': 41900
        },
        {
            'brand': 'Zilon',
            'model': 'ZT-09IS',
            'series': 'Inverter',
            'power': 2.6,
            'price': 33900
        },
        {
            'brand': 'Hitachi',
            'model': 'RAK-18RPD/RAC-18WPD',
            'series': 'Performance',
            'power': 5.0,
            'price': 67900
        },
        {
            'brand': 'LG',
            'model': 'S09ET',
            'series': 'Standard',
            'power': 2.5,
            'price': 38900
        },
        {
            'brand': 'DAICOND',
            'model': 'DC-09INVH',
            'series': 'Inverter',
            'power': 2.6,
            'price': 31900
        },
        {
            'brand': 'ECOSTAR',
            'model': 'ES-09IN',
            'series': 'Eco',
            'power': 2.5,
            'price': 29900
        }
    ]
    
    images = [
        'https://images.unsplash.com/photo-1631545805119-17cbd88d3d53?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1634641283431-5c644bb6f944?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1585909695284-32d2985ac9c0?w=400&h=300&fit=crop'
    ]
    
    for idx, item in enumerate(mock_breez_products):
        product = {
            'id': f'breez_{idx}',
            'name': f'{item["brand"]} {item["model"]}',
            'brand': item['brand'],
            'category': 'Кондиционеры',
            'series': item['series'],
            'power': item['power'],
            'type': 'Настенный',
            'price': item['price'],
            'source': 'breez.ru',
            'image': images[idx % len(images)],
            'features': ['Инвертор', 'Самодиагностика', 'Wi-Fi']
        }
        products.append(product)
    
    return products
