import { useState, useEffect } from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Checkbox } from '@/components/ui/checkbox';
import { Textarea } from '@/components/ui/textarea';
import Icon from '@/components/ui/icon';

type Product = {
  id: string;
  name: string;
  brand: string;
  category: string;
  series?: string;
  power: number;
  type: string;
  price: number;
  image: string;
  source: string;
  features?: string[];
};

const API_URL = 'https://functions.poehali.dev/09c39634-7289-4c5c-821b-a92a6e2b6b9a';

const Index = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [priceRange, setPriceRange] = useState([0, 100000]);
  const [selectedBrands, setSelectedBrands] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await fetch(API_URL);
      const data = await response.json();
      setProducts(data.products || []);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const brands = Array.from(new Set(products.map(p => p.brand))).sort();
  const types = Array.from(new Set(products.map(p => p.type))).sort();

  const filteredProducts = products.filter(product => {
    const priceMatch = product.price >= priceRange[0] && product.price <= priceRange[1];
    const brandMatch = selectedBrands.length === 0 || selectedBrands.includes(product.brand);
    const typeMatch = selectedTypes.length === 0 || selectedTypes.includes(product.type);
    return priceMatch && brandMatch && typeMatch;
  });

  const toggleBrand = (brand: string) => {
    setSelectedBrands(prev =>
      prev.includes(brand) ? prev.filter(b => b !== brand) : [...prev, brand]
    );
  };

  const toggleType = (type: string) => {
    setSelectedTypes(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log({ name, phone, message });
    setName('');
    setPhone('');
    setMessage('');
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-white sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Icon name="Snowflake" className="text-primary" size={32} />
            <h1 className="text-2xl font-bold text-foreground">КлиматПро</h1>
          </div>
          <nav className="hidden md:flex gap-6">
            <a href="#catalog" className="text-muted-foreground hover:text-primary transition-colors">Каталог</a>
            <a href="#about" className="text-muted-foreground hover:text-primary transition-colors">О нас</a>
            <a href="#contacts" className="text-muted-foreground hover:text-primary transition-colors">Контакты</a>
          </nav>
          <Button className="gap-2">
            <Icon name="Phone" size={18} />
            <span className="hidden sm:inline">Позвонить</span>
          </Button>
        </div>
      </header>

      <section className="bg-gradient-to-br from-primary/5 to-secondary/10 py-20">
        <div className="container mx-auto px-4 text-center animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">Климатическое оборудование</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
            Широкий выбор кондиционеров от ведущих производителей. Профессиональная консультация и гарантия качества.
          </p>
          <Button size="lg" className="gap-2">
            <Icon name="ArrowDown" size={20} />
            Смотреть каталог
          </Button>
        </div>
      </section>

      <section id="catalog" className="py-16">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-[280px_1fr] gap-8">
            <aside className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Icon name="SlidersHorizontal" size={20} />
                    Фильтры
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-3">
                    <Label>Цена: {priceRange[0].toLocaleString()} - {priceRange[1].toLocaleString()} ₽</Label>
                    <Slider
                      min={0}
                      max={100000}
                      step={1000}
                      value={priceRange}
                      onValueChange={setPriceRange}
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-3">
                    <Label className="font-semibold">Бренд</Label>
                    {brands.map(brand => (
                      <div key={brand} className="flex items-center space-x-2">
                        <Checkbox
                          id={brand}
                          checked={selectedBrands.includes(brand)}
                          onCheckedChange={() => toggleBrand(brand)}
                        />
                        <label htmlFor={brand} className="text-sm cursor-pointer">
                          {brand}
                        </label>
                      </div>
                    ))}
                  </div>

                  <div className="space-y-3">
                    <Label className="font-semibold">Тип установки</Label>
                    {types.map(type => (
                      <div key={type} className="flex items-center space-x-2">
                        <Checkbox
                          id={type}
                          checked={selectedTypes.includes(type)}
                          onCheckedChange={() => toggleType(type)}
                        />
                        <label htmlFor={type} className="text-sm cursor-pointer">
                          {type}
                        </label>
                      </div>
                    ))}
                  </div>

                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={() => {
                      setPriceRange([0, 100000]);
                      setSelectedBrands([]);
                      setSelectedTypes([]);
                    }}
                  >
                    Сбросить фильтры
                  </Button>
                </CardContent>
              </Card>
            </aside>

            <div>
              <div className="mb-6 flex items-center justify-between">
                <p className="text-muted-foreground">
                  Найдено товаров: <span className="font-semibold text-foreground">{filteredProducts.length}</span>
                </p>
              </div>

              {loading ? (
                <div className="flex items-center justify-center py-20">
                  <div className="text-center">
                    <Icon name="Loader2" className="animate-spin text-primary mx-auto mb-4" size={48} />
                    <p className="text-muted-foreground">Загрузка товаров...</p>
                  </div>
                </div>
              ) : (
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredProducts.map((product, index) => (
                  <Card
                    key={product.id}
                    className="overflow-hidden hover:shadow-lg transition-all duration-300 hover:-translate-y-1 animate-scale-in"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    <div className="aspect-[4/3] overflow-hidden bg-muted">
                      <img
                        src={product.image}
                        alt={product.name}
                        className="w-full h-full object-cover hover:scale-110 transition-transform duration-500"
                      />
                    </div>
                    <CardHeader>
                      <CardTitle className="text-lg">{product.name}</CardTitle>
                      <p className="text-sm text-muted-foreground">{product.brand}</p>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <div className="flex items-center gap-2 text-sm">
                        <Icon name="Zap" size={16} className="text-primary" />
                        <span>Мощность: {product.power} кВт</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <Icon name="Box" size={16} className="text-primary" />
                        <span>{product.type}</span>
                      </div>
                      {product.series && (
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <Icon name="Tag" size={16} />
                          <span>{product.series}</span>
                        </div>
                      )}
                      <div className="flex items-center gap-2 text-xs text-muted-foreground pt-1">
                        <Icon name="Database" size={14} />
                        <span>{product.source}</span>
                      </div>
                      <p className="text-2xl font-bold text-primary pt-2">
                        {product.price.toLocaleString()} ₽
                      </p>
                    </CardContent>
                    <CardFooter className="gap-2">
                      <Button className="flex-1 gap-2">
                        <Icon name="ShoppingCart" size={18} />
                        В корзину
                      </Button>
                      <Button variant="outline" size="icon">
                        <Icon name="Info" size={18} />
                      </Button>
                    </CardFooter>
                  </Card>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      <section id="contacts" className="py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-4">Свяжитесь с нами</h2>
            <p className="text-center text-muted-foreground mb-12">
              Оставьте заявку, и наши специалисты помогут подобрать оптимальное решение
            </p>

            <div className="grid md:grid-cols-2 gap-8">
              <Card>
                <CardHeader>
                  <CardTitle>Контактная информация</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-start gap-3">
                    <Icon name="Phone" className="text-primary mt-1" size={20} />
                    <div>
                      <p className="font-semibold">Телефон</p>
                      <p className="text-muted-foreground">+7 (495) 123-45-67</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Icon name="Mail" className="text-primary mt-1" size={20} />
                    <div>
                      <p className="font-semibold">Email</p>
                      <p className="text-muted-foreground">info@klimatpro.ru</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Icon name="MapPin" className="text-primary mt-1" size={20} />
                    <div>
                      <p className="font-semibold">Адрес</p>
                      <p className="text-muted-foreground">г. Москва, ул. Примерная, д. 123</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Icon name="Clock" className="text-primary mt-1" size={20} />
                    <div>
                      <p className="font-semibold">Режим работы</p>
                      <p className="text-muted-foreground">Пн-Пт: 9:00 - 18:00</p>
                      <p className="text-muted-foreground">Сб-Вс: выходной</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Форма обратной связи</CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">Имя</Label>
                      <Input
                        id="name"
                        placeholder="Ваше имя"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="phone">Телефон</Label>
                      <Input
                        id="phone"
                        type="tel"
                        placeholder="+7 (___) ___-__-__"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="message">Сообщение</Label>
                      <Textarea
                        id="message"
                        placeholder="Опишите ваш вопрос или пожелание"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        rows={4}
                        required
                      />
                    </div>
                    <Button type="submit" className="w-full gap-2">
                      <Icon name="Send" size={18} />
                      Отправить заявку
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      <footer className="bg-foreground text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <Icon name="Snowflake" size={24} />
              <span className="font-semibold">КлиматПро</span>
            </div>
            <p className="text-sm text-muted">© 2024 КлиматПро. Все права защищены.</p>
            <div className="flex gap-4">
              <a href="#" className="hover:text-primary transition-colors">
                <Icon name="Mail" size={20} />
              </a>
              <a href="#" className="hover:text-primary transition-colors">
                <Icon name="Phone" size={20} />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;