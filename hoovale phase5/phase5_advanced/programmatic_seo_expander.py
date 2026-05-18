"""
HOOVALE Programmatic SEO Expander
==================================
Scale your SEO content from 8 cities to 50+ cities (and beyond) with one script.
Same approach can scale to 200+ industry/use-case combinations.

Programmatic SEO = generating high-quality unique pages from data + templates.
Done right, can rank for thousands of long-tail keywords.
Done wrong, looks like spam to Google.

KEY PRINCIPLES (to avoid Google penalty):
1. Each page must be genuinely useful (not thin/duplicated)
2. Content must be substantially unique per page (>60% unique text)
3. Include localized data: actual delivery times, nearby areas, local industries
4. Limit creation rate (don't dump 500 pages overnight — Google flags)
5. Internal linking strategy across new pages

Place at: products/management/commands/expand_cities.py
Run: python manage.py expand_cities
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import CityPage


# ============================================================================
# CITY DATA — 50+ Indian Cities With Localized Information
# ============================================================================
# Each city has unique data points that make pages substantively different:
# - State, population, business landscape
# - Estimated delivery time from Jaipur
# - Major nearby areas
# - Primary industries that buy wall clocks
# - Local landmarks/business hubs

CITIES_DATA = [
    # === METROS (existing in Phase 2, listed for reference) ===
    # Delhi, Mumbai, Bangalore, Chennai, Hyderabad, Pune, Ahmedabad, Kolkata
    
    # === TIER-1 SUPPLEMENTS ===
    {
        'city': 'Surat', 'state': 'Gujarat', 'population': '6.5 million',
        'delivery_days': '3-4', 'nearby': 'Vapi, Navsari, Bharuch, Valsad',
        'industries': 'textile mills, diamond polishing, real estate, IT parks',
        'business_hubs': 'Adajan, Ring Road, Vesu, Athwalines',
        'local_context': 'India\'s diamond and textile capital with significant '
                          'corporate gifting culture from textile and diamond businesses',
    },
    {
        'city': 'Jaipur', 'state': 'Rajasthan', 'population': '4 million',
        'delivery_days': '1', 'nearby': 'Sikar, Ajmer, Tonk, Dausa',
        'industries': 'jewellery export, hotels, IT, education, government',
        'business_hubs': 'MI Road, C Scheme, Malviya Nagar, Vaishali Nagar',
        'local_context': 'HOOVALE\'s home city. Direct factory pickup available '
                          'for Jaipur businesses. Same-day delivery within city.',
    },
    {
        'city': 'Lucknow', 'state': 'Uttar Pradesh', 'population': '3 million',
        'delivery_days': '2-3', 'nearby': 'Kanpur, Faizabad, Sultanpur, Sitapur',
        'industries': 'government offices, education, healthcare, retail, hospitality',
        'business_hubs': 'Gomti Nagar, Hazratganj, Alambagh',
        'local_context': 'Capital of India\'s largest state. Significant government '
                          'and institutional buyer presence.',
    },
    {
        'city': 'Kanpur', 'state': 'Uttar Pradesh', 'population': '3 million',
        'delivery_days': '3', 'nearby': 'Lucknow, Unnao, Etawah, Hardoi',
        'industries': 'leather industry, manufacturing, education, retail',
        'business_hubs': 'Kakadeo, Civil Lines, Govind Nagar',
        'local_context': 'Industrial hub with strong manufacturing and B2B demand.',
    },
    {
        'city': 'Nagpur', 'state': 'Maharashtra', 'population': '2.5 million',
        'delivery_days': '3', 'nearby': 'Wardha, Amravati, Bhandara, Gondia',
        'industries': 'oranges trade, MIHAN aerospace, government, retail',
        'business_hubs': 'Civil Lines, Sitabuldi, Dharampeth, MIHAN',
        'local_context': 'Central India\'s largest commercial hub.',
    },
    {
        'city': 'Indore', 'state': 'Madhya Pradesh', 'population': '2 million',
        'delivery_days': '2', 'nearby': 'Bhopal, Ujjain, Dewas, Pithampur',
        'industries': 'pharma, automotive, IT, retail, education',
        'business_hubs': 'Vijay Nagar, MG Road, AB Road, Pipliyahana',
        'local_context': 'Commercial capital of MP. Major B2B center.',
    },
    {
        'city': 'Bhopal', 'state': 'Madhya Pradesh', 'population': '2 million',
        'delivery_days': '2-3', 'nearby': 'Indore, Sehore, Vidisha, Raisen',
        'industries': 'government, education, manufacturing, healthcare',
        'business_hubs': 'MP Nagar, Arera Colony, Bittan Market',
        'local_context': 'Government capital with strong institutional buyer base.',
    },
    {
        'city': 'Coimbatore', 'state': 'Tamil Nadu', 'population': '2 million',
        'delivery_days': '4-5', 'nearby': 'Tirupur, Erode, Pollachi, Mettupalayam',
        'industries': 'textile, engineering, education, IT, healthcare',
        'business_hubs': 'RS Puram, Race Course, Avinashi Road',
        'local_context': 'Manchester of South India. Strong manufacturing B2B.',
    },
    {
        'city': 'Vadodara', 'state': 'Gujarat', 'population': '2 million',
        'delivery_days': '2', 'nearby': 'Anand, Bharuch, Godhra, Halol',
        'industries': 'petrochemicals, engineering, pharma, IT',
        'business_hubs': 'Alkapuri, Race Course, Sayajigunj, Akota',
        'local_context': 'Industrial powerhouse with multinational presence.',
    },
    
    # === TIER-2 CITIES ===
    {
        'city': 'Visakhapatnam', 'state': 'Andhra Pradesh', 'population': '2 million',
        'delivery_days': '5-6', 'nearby': 'Vijayawada, Rajahmundry, Anakapalle',
        'industries': 'port, steel plant, IT, naval base, tourism',
        'business_hubs': 'Beach Road, Dwaraka Nagar, Siripuram',
        'local_context': 'AP\'s commercial capital and largest port city.',
    },
    {
        'city': 'Vijayawada', 'state': 'Andhra Pradesh', 'population': '1.5 million',
        'delivery_days': '5-6', 'nearby': 'Guntur, Eluru, Machilipatnam',
        'industries': 'agriculture trade, education, healthcare, retail',
        'business_hubs': 'Benz Circle, MG Road, Governorpet',
        'local_context': 'Capital region of Andhra Pradesh.',
    },
    {
        'city': 'Patna', 'state': 'Bihar', 'population': '2 million',
        'delivery_days': '4-5', 'nearby': 'Muzaffarpur, Gaya, Bhagalpur',
        'industries': 'government, education, healthcare, retail',
        'business_hubs': 'Boring Road, Bailey Road, Patna City',
        'local_context': 'Bihar\'s capital with growing commercial activity.',
    },
    {
        'city': 'Raipur', 'state': 'Chhattisgarh', 'population': '1.5 million',
        'delivery_days': '4', 'nearby': 'Bhilai, Durg, Bilaspur',
        'industries': 'steel, power, agriculture, government',
        'business_hubs': 'Pandri, Telibandha, Civil Lines',
        'local_context': 'Chhattisgarh\'s commercial capital.',
    },
    {
        'city': 'Ranchi', 'state': 'Jharkhand', 'population': '1.5 million',
        'delivery_days': '4-5', 'nearby': 'Jamshedpur, Dhanbad, Bokaro',
        'industries': 'government, mining, education, healthcare',
        'business_hubs': 'Main Road, Lalpur, Doranda',
        'local_context': 'Jharkhand\'s capital with significant institutional buyers.',
    },
    {
        'city': 'Jamshedpur', 'state': 'Jharkhand', 'population': '1.5 million',
        'delivery_days': '4-5', 'nearby': 'Ranchi, Dhanbad, Asansol',
        'industries': 'steel (Tata Steel), automotive, engineering',
        'business_hubs': 'Bistupur, Sakchi, Sonari',
        'local_context': 'Steel city with major industrial B2B base.',
    },
    {
        'city': 'Bhubaneswar', 'state': 'Odisha', 'population': '1 million',
        'delivery_days': '5', 'nearby': 'Cuttack, Puri, Khordha',
        'industries': 'IT, government, education, tourism',
        'business_hubs': 'Saheed Nagar, Patia, Nayapalli',
        'local_context': 'Odisha\'s capital and emerging IT hub.',
    },
    {
        'city': 'Thiruvananthapuram', 'state': 'Kerala', 'population': '1 million',
        'delivery_days': '5-6', 'nearby': 'Kollam, Kochi, Kanyakumari',
        'industries': 'IT (Technopark), government, tourism, healthcare',
        'business_hubs': 'Technopark, Kowdiar, MG Road',
        'local_context': 'Kerala\'s capital with major IT and government sector.',
    },
    {
        'city': 'Kochi', 'state': 'Kerala', 'population': '2 million',
        'delivery_days': '5-6', 'nearby': 'Aluva, Cherthala, Vypin',
        'industries': 'port, IT (InfoPark), tourism, retail',
        'business_hubs': 'MG Road, Marine Drive, InfoPark',
        'local_context': 'Commercial hub of Kerala.',
    },
    {
        'city': 'Chandigarh', 'state': 'Punjab/Haryana', 'population': '1 million',
        'delivery_days': '2', 'nearby': 'Mohali, Panchkula, Zirakpur',
        'industries': 'IT, government, education, retail',
        'business_hubs': 'Sector 17, IT Park, Industrial Area',
        'local_context': 'Capital of Punjab and Haryana, planned modern city.',
    },
    {
        'city': 'Ludhiana', 'state': 'Punjab', 'population': '1.6 million',
        'delivery_days': '2-3', 'nearby': 'Jalandhar, Amritsar, Patiala',
        'industries': 'manufacturing (textile, machinery), retail',
        'business_hubs': 'Bharat Nagar Chowk, Model Town, Ghumar Mandi',
        'local_context': 'Punjab\'s industrial powerhouse.',
    },
    {
        'city': 'Amritsar', 'state': 'Punjab', 'population': '1.2 million',
        'delivery_days': '3', 'nearby': 'Jalandhar, Pathankot, Tarn Taran',
        'industries': 'tourism (Golden Temple), trade, textile',
        'business_hubs': 'Hall Bazaar, Lawrence Road, GT Road',
        'local_context': 'Sikh religious center with strong tourism economy.',
    },
    
    # === TIER-3 (Strategic Long-Tail) ===
    {
        'city': 'Jodhpur', 'state': 'Rajasthan', 'population': '1.4 million',
        'delivery_days': '1-2', 'nearby': 'Bikaner, Pali, Nagaur',
        'industries': 'handicrafts, tourism, government, trade',
        'business_hubs': 'Sardarpura, Ratanada, High Court Road',
        'local_context': 'Rajasthan\'s second-largest city. 1-day delivery from Jaipur.',
    },
    {
        'city': 'Udaipur', 'state': 'Rajasthan', 'population': '700K',
        'delivery_days': '2', 'nearby': 'Chittorgarh, Banswara, Rajsamand',
        'industries': 'tourism, marble industry, education',
        'business_hubs': 'Chetak Circle, Bhupalpura, Sukher',
        'local_context': 'Premier tourism city with luxury hotels.',
    },
    {
        'city': 'Ajmer', 'state': 'Rajasthan', 'population': '600K',
        'delivery_days': '1', 'nearby': 'Pushkar, Beawar, Tonk',
        'industries': 'tourism (Dargah), education, trade',
        'business_hubs': 'Madar Gate, Civil Lines, Vaishali Nagar',
        'local_context': 'Adjacent to Jaipur. Strong religious tourism economy.',
    },
    {
        'city': 'Kota', 'state': 'Rajasthan', 'population': '1 million',
        'delivery_days': '2', 'nearby': 'Bundi, Jhalawar, Baran',
        'industries': 'coaching institutes, manufacturing, agriculture',
        'business_hubs': 'Rajiv Gandhi Nagar, Talwandi, Vigyan Nagar',
        'local_context': 'India\'s coaching capital with major education economy.',
    },
    {
        'city': 'Gwalior', 'state': 'Madhya Pradesh', 'population': '1.1 million',
        'delivery_days': '2-3', 'nearby': 'Shivpuri, Datia, Bhind',
        'industries': 'government, education, tourism, manufacturing',
        'business_hubs': 'City Centre, Phool Bagh, Morar',
        'local_context': 'Historic city with growing commerce.',
    },
    {
        'city': 'Jabalpur', 'state': 'Madhya Pradesh', 'population': '1.3 million',
        'delivery_days': '3-4', 'nearby': 'Katni, Mandla, Seoni',
        'industries': 'defence, manufacturing, tourism, education',
        'business_hubs': 'Civil Lines, Russel Chowk, Wright Town',
        'local_context': 'Defence and industrial hub.',
    },
    {
        'city': 'Madurai', 'state': 'Tamil Nadu', 'population': '1.6 million',
        'delivery_days': '5-6', 'nearby': 'Theni, Dindigul, Sivaganga',
        'industries': 'temple tourism, textile, IT, education',
        'business_hubs': 'Anna Nagar, K K Nagar, Town Hall Road',
        'local_context': 'Temple city with strong tourism and textile economy.',
    },
    {
        'city': 'Tirunelveli', 'state': 'Tamil Nadu', 'population': '500K',
        'delivery_days': '6', 'nearby': 'Tirupur, Madurai, Kanyakumari',
        'industries': 'agriculture trade, education, textile, retail',
        'business_hubs': 'Palayamkottai, Kallidaikurichi',
        'local_context': 'South Tamil Nadu commercial center.',
    },
    {
        'city': 'Mysore', 'state': 'Karnataka', 'population': '900K',
        'delivery_days': '5', 'nearby': 'Mandya, Hassan, Chamarajanagar',
        'industries': 'tourism, IT, traditional industries, education',
        'business_hubs': 'Sayyaji Rao Road, Vinoba Road',
        'local_context': 'Heritage city with growing IT presence.',
    },
    {
        'city': 'Mangalore', 'state': 'Karnataka', 'population': '600K',
        'delivery_days': '5-6', 'nearby': 'Udupi, Kasaragod, Kundapur',
        'industries': 'port, education, IT, healthcare',
        'business_hubs': 'Hampankatta, Lalbagh, Ballalbagh',
        'local_context': 'Major port and education hub.',
    },
    {
        'city': 'Hubli', 'state': 'Karnataka', 'population': '950K',
        'delivery_days': '5', 'nearby': 'Dharwad, Belgaum, Gadag',
        'industries': 'trade, textile, education, agriculture',
        'business_hubs': 'Lamington Road, Vidya Nagar',
        'local_context': 'North Karnataka commercial hub.',
    },
    {
        'city': 'Guwahati', 'state': 'Assam', 'population': '1 million',
        'delivery_days': '6-7', 'nearby': 'Tezpur, Dibrugarh, Silchar',
        'industries': 'government, tea, oil refining, retail',
        'business_hubs': 'Paltan Bazaar, GS Road, Beltola',
        'local_context': 'Northeast India\'s gateway and largest city.',
    },
    {
        'city': 'Dehradun', 'state': 'Uttarakhand', 'population': '700K',
        'delivery_days': '3', 'nearby': 'Mussoorie, Haridwar, Rishikesh',
        'industries': 'government, education, tourism, IT',
        'business_hubs': 'Rajpur Road, Paltan Bazaar, GMS Road',
        'local_context': 'Uttarakhand capital and education hub.',
    },
    {
        'city': 'Haridwar', 'state': 'Uttarakhand', 'population': '300K',
        'delivery_days': '3', 'nearby': 'Rishikesh, Dehradun, Roorkee',
        'industries': 'tourism (pilgrim), pharmaceuticals, education',
        'business_hubs': 'Har Ki Pauri area, Bhupatwala',
        'local_context': 'Major pilgrimage destination.',
    },
    {
        'city': 'Aurangabad', 'state': 'Maharashtra', 'population': '1.5 million',
        'delivery_days': '3-4', 'nearby': 'Jalna, Nashik, Beed',
        'industries': 'auto manufacturing, education, tourism',
        'business_hubs': 'CIDCO, Garkheda, Beed Bypass',
        'local_context': 'Industrial hub with major automotive companies.',
    },
    {
        'city': 'Nashik', 'state': 'Maharashtra', 'population': '1.5 million',
        'delivery_days': '3', 'nearby': 'Aurangabad, Pune, Ahmednagar',
        'industries': 'wine, manufacturing, agriculture, religious tourism',
        'business_hubs': 'College Road, MG Road, Govind Nagar',
        'local_context': 'India\'s wine capital and pilgrimage destination.',
    },
    {
        'city': 'Solapur', 'state': 'Maharashtra', 'population': '1 million',
        'delivery_days': '3-4', 'nearby': 'Pandharpur, Akkalkot, Latur',
        'industries': 'textile, agriculture, beedi industry',
        'business_hubs': 'Murarji Peth, North Solapur',
        'local_context': 'Textile and agricultural commerce center.',
    },
    {
        'city': 'Vijayawada', 'state': 'Andhra Pradesh', 'population': '1.5 million',
        'delivery_days': '5-6', 'nearby': 'Guntur, Eluru, Machilipatnam',
        'industries': 'agriculture, education, trade, healthcare',
        'business_hubs': 'Benz Circle, MG Road, Governorpet',
        'local_context': 'Andhra Pradesh\'s commercial heart.',
    },
    {
        'city': 'Tirupati', 'state': 'Andhra Pradesh', 'population': '400K',
        'delivery_days': '6', 'nearby': 'Chittoor, Tirumala, Sri Kalahasti',
        'industries': 'religious tourism, education, IT',
        'business_hubs': 'Tirupati Main Road, RC Road',
        'local_context': 'Major pilgrimage destination with strong tourism economy.',
    },
    {
        'city': 'Warangal', 'state': 'Telangana', 'population': '800K',
        'delivery_days': '5', 'nearby': 'Karimnagar, Khammam, Hanamkonda',
        'industries': 'education, agriculture, textile, retail',
        'business_hubs': 'Hanamkonda, Kazipet',
        'local_context': 'Second-largest city in Telangana.',
    },
    {
        'city': 'Faridabad', 'state': 'Haryana', 'population': '1.5 million',
        'delivery_days': '1-2', 'nearby': 'Delhi NCR (Gurgaon, Noida)',
        'industries': 'manufacturing, automotive, IT, real estate',
        'business_hubs': 'Sector 15, NIT, Industrial Area',
        'local_context': 'Major industrial hub in NCR.',
    },
    {
        'city': 'Gurgaon', 'state': 'Haryana', 'population': '900K',
        'delivery_days': '1-2', 'nearby': 'Delhi, Manesar, Sohna',
        'industries': 'IT, BPO, automotive, real estate, finance',
        'business_hubs': 'Cyber Hub, Golf Course Road, MG Road',
        'local_context': 'Millennium City with major MNC presence.',
    },
    {
        'city': 'Noida', 'state': 'Uttar Pradesh', 'population': '900K',
        'delivery_days': '1-2', 'nearby': 'Delhi, Ghaziabad, Greater Noida',
        'industries': 'IT, media, manufacturing, education',
        'business_hubs': 'Sector 18, Sector 62, Film City',
        'local_context': 'NCR\'s IT and corporate hub.',
    },
    {
        'city': 'Allahabad', 'state': 'Uttar Pradesh', 'population': '1.2 million',
        'delivery_days': '4', 'nearby': 'Varanasi, Lucknow, Kanpur',
        'industries': 'education, government, religious tourism',
        'business_hubs': 'Civil Lines, Katra, Allahpur',
        'local_context': 'Historic education and religious city (Prayagraj).',
    },
    {
        'city': 'Varanasi', 'state': 'Uttar Pradesh', 'population': '1.5 million',
        'delivery_days': '4', 'nearby': 'Allahabad, Mirzapur, Mughalsarai',
        'industries': 'religious tourism, weaving, education',
        'business_hubs': 'Sigra, Mahmoorganj, Lanka',
        'local_context': 'India\'s spiritual capital with strong tourism.',
    },
    {
        'city': 'Meerut', 'state': 'Uttar Pradesh', 'population': '1.5 million',
        'delivery_days': '2', 'nearby': 'Delhi, Ghaziabad, Muzaffarnagar',
        'industries': 'sports goods, scissors, manufacturing',
        'business_hubs': 'Sadar Bazaar, Begum Bridge, Civil Lines',
        'local_context': 'Sports goods manufacturing capital.',
    },
    {
        'city': 'Agra', 'state': 'Uttar Pradesh', 'population': '1.8 million',
        'delivery_days': '2', 'nearby': 'Mathura, Aligarh, Firozabad',
        'industries': 'tourism (Taj Mahal), leather, marble',
        'business_hubs': 'Sanjay Place, Sadar Bazaar, MG Road',
        'local_context': 'Major tourism city with significant hospitality sector.',
    },
    
    # === REGIONAL POWERHOUSES ===
    {
        'city': 'Salem', 'state': 'Tamil Nadu', 'population': '900K',
        'delivery_days': '5', 'nearby': 'Erode, Namakkal, Dharmapuri',
        'industries': 'steel, textile, mango trade, education',
        'business_hubs': 'Old Bus Stand, Junction Main Road',
        'local_context': 'Steel and industrial hub of Tamil Nadu.',
    },
    {
        'city': 'Rajkot', 'state': 'Gujarat', 'population': '1.5 million',
        'delivery_days': '2-3', 'nearby': 'Jamnagar, Junagadh, Morbi',
        'industries': 'automotive, machinery, jewellery, education',
        'business_hubs': 'Race Course Road, Yagnik Road, University Road',
        'local_context': 'Gujarat\'s fourth-largest city, major manufacturing.',
    },
    {
        'city': 'Trichy', 'state': 'Tamil Nadu', 'population': '900K',
        'delivery_days': '5-6', 'nearby': 'Thanjavur, Pudukkottai, Karur',
        'industries': 'education, BHEL, textile, religious tourism',
        'business_hubs': 'NSB Road, Cantonment, K K Nagar',
        'local_context': 'Education and BHEL hub.',
    },
]


# ============================================================================
# CONTENT GENERATION TEMPLATES
# ============================================================================

INTRO_TEMPLATES = [
    "HOOVALE is a premier wall clock manufacturer based in Jaipur, supplying "
    "retailers, hotels, hospitals, corporates, and bulk buyers across {city}. "
    "With {delivery_days}-day delivery from our Jaipur factory, we serve businesses "
    "throughout {state} including {nearby}.",
    
    "Looking for a reliable wall clock supplier in {city}? HOOVALE is a {state}-based "
    "manufacturer offering bulk wall clock supply, custom logo printing, and OEM "
    "manufacturing with direct factory pricing. We deliver to {city} and surrounding "
    "areas ({nearby}) within {delivery_days} days.",
    
    "{city} businesses choose HOOVALE for premium wall clocks at factory-direct "
    "prices. Located in {state}, we serve {city}'s {industries} sectors with bulk "
    "supply, custom branding, and timely delivery (within {delivery_days} days).",
]

WHY_CHOOSE_TEMPLATES = [
    "## Why HOOVALE for Wall Clocks in {city}?\n\n"
    "**Factory-direct pricing** — 30-50% lower than retail in {city}\n"
    "**{delivery_days}-day delivery** from Jaipur to {city}\n"
    "**Custom logo printing** — free above 200 pieces\n"
    "**MOQ flexibility** — start from 100 pieces\n"
    "**Bulk pricing tiers** — better rates with larger orders\n"
    "**Quality guarantee** — 1-year warranty on all clocks\n"
    "**Personalised service** — direct WhatsApp/call support\n\n"
    "We've supplied wall clocks to {city}'s {industries} businesses, with "
    "consistent reliability for both first-time and repeat customers.",
]

INDUSTRIES_TEMPLATES = [
    "## Industries We Serve in {city}\n\n"
    "{city}'s diverse business landscape includes {industries}. HOOVALE supplies "
    "wall clocks for:\n\n"
    "🏢 **Corporate offices and IT parks** — branded conference room clocks, "
    "executive cabin pieces, designer reception clocks\n\n"
    "🏨 **Hotels and hospitality** — silent sweep room clocks, designer lobby pieces, "
    "multi-time-zone configurations for business hotels\n\n"
    "🏥 **Hospitals and healthcare** — non-tick patient ward clocks, hygiene-compatible "
    "designs, high-visibility OPD waiting area clocks\n\n"
    "🎓 **Schools and educational institutions** — durable classroom clocks, branded "
    "options for premium private schools\n\n"
    "🛍️ **Retailers and gift shops** — wholesale supply with mixed-design orders\n\n"
    "🏠 **Real estate developers** — flat owner handover gifting at scale\n\n"
    "Businesses across {business_hubs} in {city} are HOOVALE's regular customers.",
]

DELIVERY_TEMPLATES = [
    "## Delivery to {city}\n\n"
    "**Standard delivery time:** {delivery_days} days from order confirmation\n"
    "**Nearby areas served:** {nearby}\n"
    "**Business hub deliveries:** {business_hubs}\n\n"
    "We use trusted logistics partners ensuring safe delivery to {city}. For bulk "
    "orders (500+ pieces), we offer special freight arrangements with comprehensive "
    "insurance coverage. Same-day pickup available for Jaipur-based customers.\n\n"
    "**Tracking:** Every order ships with tracking number shared via WhatsApp. "
    "Real-time updates from dispatch to delivery.",
]


def _generate_unique_seo_content(city_data):
    """Generate substantively unique content for a city page."""
    import random
    
    # Use city-specific data to ensure uniqueness
    city = city_data['city']
    state = city_data['state']
    delivery_days = city_data['delivery_days']
    nearby = city_data['nearby']
    industries = city_data['industries']
    business_hubs = city_data['business_hubs']
    local_context = city_data['local_context']
    
    # Rotate templates for variety
    intro = random.choice(INTRO_TEMPLATES).format(**city_data)
    why_choose = WHY_CHOOSE_TEMPLATES[0].format(**city_data)
    industries_content = INDUSTRIES_TEMPLATES[0].format(**city_data)
    delivery_content = DELIVERY_TEMPLATES[0].format(**city_data)
    
    closing = (
        f"## Order Wall Clocks for Your {city} Business Today\n\n"
        f"Whether you're a retailer in {city} looking for wholesale supply, a hotel "
        f"in {state} needing room clocks, a corporate planning bulk gifting, or a "
        f"school upgrading classrooms — HOOVALE is your direct manufacturer.\n\n"
        f"{local_context}\n\n"
        f"📞 Call/WhatsApp: +91 9462207356\n"
        f"📧 Email: info@hoovale.com\n"
        f"🌐 Catalogue: hoovale.com\n\n"
        f"Get pricing for your {city} requirement within 2 hours during business days."
    )
    
    full_content = f"{intro}\n\n{why_choose}\n\n{industries_content}\n\n{delivery_content}\n\n{closing}"
    
    return {
        'intro_content': intro,
        'why_choose_content': why_choose,
        'industries_content': industries_content,
        'delivery_content': delivery_content,
        'closing_content': closing,
        'full_content': full_content,
    }


# ============================================================================
# COMMAND CLASS
# ============================================================================
class Command(BaseCommand):
    help = 'Programmatic SEO: expand HOOVALE to 50+ city pages'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of cities to create (e.g., --limit 10 for first 10)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without saving'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            default=True,
            help='Skip cities that already exist'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            '🚀 HOOVALE Programmatic SEO Expander\n'
            '====================================\n'
        ))
        
        cities_to_process = CITIES_DATA[:options['limit']] if options['limit'] else CITIES_DATA
        
        created_count = 0
        skipped_count = 0
        
        for city_data in cities_to_process:
            city = city_data['city']
            slug = slugify(f"wall-clock-supplier-in-{city}")
            
            # Check if exists
            existing = CityPage.objects.filter(slug=slug).first()
            if existing and options['skip_existing']:
                self.stdout.write(f"   ⏭️  Skipping (exists): {city}")
                skipped_count += 1
                continue
            
            # Generate content
            content = _generate_unique_seo_content(city_data)
            
            if options['dry_run']:
                self.stdout.write(f"\n📄 Would create: {city}")
                self.stdout.write(f"   Slug: {slug}")
                self.stdout.write(f"   Content length: {len(content['full_content'])} chars")
                continue
            
            # Create city page (adapt to your actual CityPage model fields)
            try:
                page = CityPage.objects.create(
                    city_name=city,
                    state=city_data['state'],
                    slug=slug,
                    page_type='supplier',
                    h1_heading=f"Wall Clock Supplier in {city} | HOOVALE Manufacturer",
                    hero_subheading=f"Premium wall clocks delivered to {city} from our Jaipur factory in {city_data['delivery_days']} days",
                    intro_content=content['intro_content'],
                    why_choose_content=content['why_choose_content'],
                    services_content=f"Bulk supply, custom logo printing, OEM manufacturing — all available for {city} businesses.",
                    delivery_content=content['delivery_content'],
                    industries_content=content['industries_content'],
                    closing_content=content['closing_content'],
                    meta_title=f"Wall Clock Supplier in {city} | HOOVALE Manufacturer in Jaipur"[:70],
                    meta_description=f"Premium wall clock supplier in {city}. Bulk supply, custom logos, {city_data['delivery_days']}-day delivery from Jaipur factory. Get quote on WhatsApp."[:160],
                    meta_keywords=f"wall clock supplier {city}, wall clock manufacturer {city}, bulk wall clocks {city}, wholesale wall clocks {state}, {city} wall clock",
                    delivery_time=f"{city_data['delivery_days']} days",
                    nearby_areas=city_data['nearby'],
                    display_order=999,  # Push these to end after existing 8 metros
                    is_active=True,
                )
                
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"   ✅ Created: {city} ({city_data['state']}) — {city_data['delivery_days']} days"
                ))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ Failed for {city}: {e}"))
        
        # Summary
        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Expansion complete!\n"
            f"   Created: {created_count} new city pages\n"
            f"   Skipped: {skipped_count} existing\n"
            f"   Total cities now: {CityPage.objects.count()}\n"
        ))
        
        self.stdout.write(self.style.WARNING(
            '\n📋 IMPORTANT NEXT STEPS:\n'
            '1. Review created pages in admin: /admin/products/citypage/\n'
            '2. Update sitemap: visit /sitemap.xml — should now show all cities\n'
            '3. Submit updated sitemap to Google Search Console\n'
            '4. Add internal links from existing high-authority pages to new cities\n'
            '5. Monitor indexing in Search Console — Google takes 1-4 weeks to index new pages\n'
            '6. DO NOT create more than 50 pages at a time (Google flags rapid expansion)\n'
            '\n⚠️ ANTI-SPAM REMINDERS:\n'
            '• If you want to add more cities, run in batches monthly\n'
            '• Ensure each page is genuinely useful (not duplicative)\n'
            '• Build internal links from blog posts to new city pages\n'
            '• Add unique testimonials/case studies per city where possible\n'
            '• Monitor for thin content warnings in Search Console\n'
        ))


# ============================================================================
# PROGRAMMATIC SEO BEST PRACTICES (Reference Documentation)
# ============================================================================
"""
SCALING STRATEGY:

This script adds ~50 cities. Combined with Phase 2's 8 metros, you'd have 58 city pages.

Can scale further to:
- Industry × City combinations (6 industries × 50 cities = 300 pages)
  e.g., /wall-clocks-for-hotels-in-{city}/
- Service × City combinations (5 services × 50 cities = 250 pages)
  e.g., /bulk-wall-clock-supply-{city}/
- Product × Use Case combinations (14 categories × 6 industries = 84 pages)
  e.g., /wooden-wall-clocks-for-hotels/

Total potential: 600+ unique pages.

CAUTION:
1. NEVER dump all 600 pages at once — Google flags as spam
2. Roll out monthly batches of 20-50 new pages
3. Each batch should be live for 2-4 weeks before next batch
4. Monitor Search Console for any "indexed though blocked" or thin content warnings
5. If any pages don't rank within 6 months, audit content quality
6. Build internal links FROM existing pages TO new pages

TIMELINE:
- Month 1: Run this script (50 cities)
- Month 2: Audit performance, fix any issues
- Month 3: Add industry × city pages for top 20 cities (20 pages)
- Month 4: Add more cities (50 more) if performance good
- Month 6+: Scale to 200+ pages

MEASURING SUCCESS:
- New city pages should appear in search within 4-8 weeks
- Long-tail keyword rankings ("wall clock supplier in [city]") within 3-6 months
- Aggregate traffic should grow noticeably by month 3-4
- Conversion rates from new pages should be comparable to existing city pages

ALTERNATIVE PROGRAMMATIC PATTERNS:
- "Wall clocks for [industry] in [city]"
- "Bulk wall clock [service] [city]"
- "Buy wall clocks online in [city]"
- "Wall clock manufacturer near [landmark]"

Each pattern can be templated and scaled if the resulting pages are genuinely useful.
"""
