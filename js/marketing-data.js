/**
 * Digital Marketing Clients Database
 */

const CLIENTS_DATA = [
  {
    "id": "dm-01",
    "name": "Magic Mirror",
    "domain": "instagram.com/magicmirrorbs",
    "url": "https://www.instagram.com/magicmirrorbs",
    "type": "custom",
    "category": "Health, Fitness & Wellness",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Beauty", "Salon"]
  },
  {
    "id": "dm-02",
    "name": "Indus",
    "domain": "instagram.com/indusjewellers",
    "url": "https://www.instagram.com/indusjewellers",
    "type": "custom",
    "category": "Luxury, Jewelry & Perfumes",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Jewelry"]
  },
  {
    "id": "dm-03",
    "name": "Silvan global",
    "domain": "instagram.com/silvanglobaluae",
    "url": "https://www.instagram.com/silvanglobaluae",
    "type": "custom",
    "category": "Corporate & Business Services",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Global"]
  },
  {
    "id": "dm-04",
    "name": "Projectivity",
    "domain": "instagram.com/projectivitytechnologies",
    "url": "https://www.instagram.com/projectivitytechnologies",
    "type": "custom",
    "category": "Technology & IT Solutions",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Tech", "IT"]
  },
  {
    "id": "dm-05",
    "name": "Navratna Jewellery",
    "domain": "instagram.com/navratnajewellery_uae",
    "url": "https://www.instagram.com/navratnajewellery_uae",
    "type": "custom",
    "category": "Luxury, Jewelry & Perfumes",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Jewelry"]
  },
  {
    "id": "dm-06",
    "name": "Al Rashad",
    "domain": "instagram.com/alrashad_commercial",
    "url": "https://www.instagram.com/alrashad_commercial",
    "type": "custom",
    "category": "Corporate & Business Services",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Commercial"]
  },
  {
    "id": "dm-07",
    "name": "KMA",
    "domain": "instagram.com/kmaroyalcarcare",
    "url": "https://www.instagram.com/kmaroyalcarcare",
    "type": "custom",
    "category": "Industrial, Trading & Engineering",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Car Care", "Automotive"]
  },
  {
    "id": "dm-08",
    "name": "Zeredia",
    "domain": "instagram.com/zeredialuxurystays",
    "url": "https://www.instagram.com/zeredialuxurystays",
    "type": "custom",
    "category": "Travel, Tourism & Hospitality",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Luxury Stays", "Hospitality"]
  },
  {
    "id": "dm-09",
    "name": "Kenz",
    "domain": "instagram.com/kenz__trading",
    "url": "https://www.instagram.com/kenz__trading",
    "type": "custom",
    "category": "Industrial, Trading & Engineering",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Trading"]
  },
  {
    "id": "dm-10",
    "name": "Leather Doctor",
    "domain": "instagram.com/theleatherdoctorabudhabi",
    "url": "https://www.instagram.com/theleatherdoctorabudhabi",
    "type": "custom",
    "category": "Corporate & Business Services",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Leather", "Repair"]
  },
  {
    "id": "dm-11",
    "name": "Shades",
    "domain": "instagram.com/shadesuniforms",
    "url": "https://www.instagram.com/shadesuniforms",
    "type": "custom",
    "category": "Fashion, Apparel & Textiles",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Uniforms", "Apparel"]
  },
  {
    "id": "dm-12",
    "name": "GRO",
    "domain": "instagram.com/grovisionrealestatellc",
    "url": "https://www.instagram.com/grovisionrealestatellc",
    "type": "custom",
    "category": "Real Estate & Interior Design",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Real Estate"]
  },
  {
    "id": "dm-13",
    "name": "1 Point 360",
    "domain": "instagram.com/1point360",
    "url": "https://www.instagram.com/1point360",
    "type": "custom",
    "category": "Creative Agency & Media",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Media"]
  },
  {
    "id": "dm-14",
    "name": "Alibjai watches",
    "domain": "instagram.com/tickwellwatches",
    "url": "https://www.instagram.com/tickwellwatches",
    "type": "custom",
    "category": "Luxury, Jewelry & Perfumes",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Watches"]
  },
  {
    "id": "dm-15",
    "name": "800 Grills",
    "domain": "instagram.com/800grills_",
    "url": "https://www.instagram.com/800grills_",
    "type": "custom",
    "category": "Food & Beverage / Dining",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Grills", "Restaurant"]
  },
  {
    "id": "dm-16",
    "name": "Liza Vend",
    "domain": "instagram.com/liza_vend",
    "url": "https://www.instagram.com/liza_vend",
    "type": "custom",
    "category": "Food & Beverage / Dining",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Vending", "Coffee"]
  },
  {
    "id": "dm-17",
    "name": "Hot Shay",
    "domain": "instagram.com/hotshayuae",
    "url": "https://www.instagram.com/hotshayuae",
    "type": "custom",
    "category": "Food & Beverage / Dining",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Beverage"]
  },
  {
    "id": "dm-18",
    "name": "Sallah Laundry",
    "domain": "instagram.com/sallah_laundry",
    "url": "https://www.instagram.com/sallah_laundry",
    "type": "custom",
    "category": "Corporate & Business Services",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Laundry"]
  },
  {
    "id": "dm-19",
    "name": "Orbiz",
    "domain": "instagram.com/orbizhive",
    "url": "https://www.instagram.com/orbizhive",
    "type": "custom",
    "category": "Real Estate & Interior Design",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Furniture"]
  },
  {
    "id": "dm-20",
    "name": "Gala",
    "domain": "instagram.com/galaitc",
    "url": "https://www.instagram.com/galaitc",
    "type": "custom",
    "category": "Technology & IT Solutions",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["ITC"]
  },
  {
    "id": "dm-21",
    "name": "ASR Zabeel",
    "domain": "instagram.com/asr_zabeel_printing",
    "url": "https://www.instagram.com/asr_zabeel_printing",
    "type": "custom",
    "category": "Creative Agency & Media",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Printing"]
  },
  {
    "id": "dm-22",
    "name": "Masterplus",
    "domain": "instagram.com/masterplusadvertisement",
    "url": "https://www.instagram.com/masterplusadvertisement",
    "type": "custom",
    "category": "Creative Agency & Media",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Advertisement"]
  },
  {
    "id": "dm-23",
    "name": "Wroom",
    "domain": "instagram.com/wroom_luxury",
    "url": "https://www.instagram.com/wroom_luxury",
    "type": "custom",
    "category": "Travel, Tourism & Hospitality",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Luxury", "Car Rental"]
  },
  {
    "id": "dm-24",
    "name": "Docit",
    "domain": "instagram.com/docit.ae",
    "url": "https://www.instagram.com/docit.ae",
    "type": "custom",
    "category": "Technology & IT Solutions",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Tech"]
  },
  {
    "id": "dm-25",
    "name": "Superstar",
    "domain": "instagram.com/super_star__fragrance",
    "url": "https://www.instagram.com/super_star__fragrance",
    "type": "custom",
    "category": "Luxury, Jewelry & Perfumes",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Fragrance"]
  },
  {
    "id": "dm-26",
    "name": "Napoli",
    "domain": "instagram.com/nappoli_furnitureco",
    "url": "https://www.instagram.com/nappoli_furnitureco",
    "type": "custom",
    "category": "Real Estate & Interior Design",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Furniture"]
  },
  {
    "id": "dm-27",
    "name": "Zarif",
    "domain": "instagram.com/zarifhairstudio",
    "url": "https://www.instagram.com/zarifhairstudio",
    "type": "custom",
    "category": "Health, Fitness & Wellness",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Hair Studio"]
  },
  {
    "id": "dm-28",
    "name": "Zaahi",
    "domain": "instagram.com/zaahi_designs",
    "url": "https://www.instagram.com/zaahi_designs",
    "type": "custom",
    "category": "Creative Agency & Media",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Designs"]
  },
  {
    "id": "dm-29",
    "name": "Adam",
    "domain": "instagram.com/adam_toursandtravels",
    "url": "https://www.instagram.com/adam_toursandtravels",
    "type": "custom",
    "category": "Travel, Tourism & Hospitality",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Tours", "Travels"]
  },
  {
    "id": "dm-30",
    "name": "Air Imarah",
    "domain": "instagram.com/airimarah.ae",
    "url": "https://www.instagram.com/airimarah.ae",
    "type": "custom",
    "category": "Travel, Tourism & Hospitality",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Aviation", "Travel"]
  },
  {
    "id": "dm-31",
    "name": "Taxbay",
    "domain": "instagram.com/taxbay.ae",
    "url": "https://www.instagram.com/taxbay.ae",
    "type": "custom",
    "category": "Corporate & Business Services",
    "platform": "Instagram",
    "status": "Active",
    "tags": ["Tax", "Accounting"]
  }
];
