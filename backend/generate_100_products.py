import json
import csv
import os

products = [
    # --- ELECTRONICS (25 Products) ---
    {
        "sku": "ELEC-HEAD-001", "name": "AuraSound Pro Wireless Headphones", "brand": "AuraSound",
        "category": "Electronics", "price": 199.99, "currency": "USD",
        "features": ["Active Noise Cancellation", "40-hour Battery Life", "Spatial Audio", "Multipoint Bluetooth 5.3"],
        "specifications": {"Driver Size": "40mm", "Weight": "250g", "Charging": "USB-C Fast Charge", "Color": "Matte Black"},
        "target_audience": "Audiophiles, remote workers, and frequent travelers",
        "primary_keywords": ["wireless noise cancelling headphones", "over ear headphones"],
        "secondary_keywords": ["bluetooth headset", "long battery headphones"],
        "usp": "Studio-grade acoustics with hybrid noise cancellation technology",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80",
        "material": "Magnesium Alloy & Memory Foam", "dimensions": "7.5 x 6.2 x 3.1 inches", "color": "Matte Black", "weight": "250g"
    },
    {
        "sku": "ELEC-WATCH-002", "name": "PulseTrack V4 Smart Fitness Watch", "brand": "PulseTrack",
        "category": "Electronics", "price": 149.50, "currency": "USD",
        "features": ["Continuous SpO2 & ECG Monitor", "50m Water Resistance", "GPS Tracking", "7-Day Battery"],
        "specifications": {"Display": "1.4-inch AMOLED", "Sensors": "Heart Rate, Optical, Accelerometer", "Compatibility": "iOS & Android"},
        "target_audience": "Athletes, runners, and fitness enthusiasts",
        "primary_keywords": ["smart fitness watch", "health tracker watch"],
        "secondary_keywords": ["waterproof smartwatch", "gps activity tracker"],
        "usp": "Medical-grade accuracy in an ultralight waterproof watch",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80",
        "material": "Aluminum & Silicone Band", "dimensions": "1.6 x 1.4 x 0.4 inches", "color": "Midnight Blue", "weight": "42g"
    },
    {
        "sku": "ELEC-SPKR-003", "name": "VibePulse 360 Portable Speaker", "brand": "VibePulse",
        "category": "Electronics", "price": 89.99, "currency": "USD",
        "features": ["360-Degree Surround Sound", "IP67 Dust & Water Proof", "PartyConnect Sync", "20-Hour Playtime"],
        "specifications": {"Output Power": "30W RMS", "Bluetooth": "5.2", "Battery": "5200mAh"},
        "target_audience": "Outdoor adventurers, party hosts, and beachgoers",
        "primary_keywords": ["portable bluetooth speaker", "waterproof outdoor speaker"],
        "secondary_keywords": ["360 degree speaker", "loud wireless speaker"],
        "usp": "Deep booming bass in a floating waterproof enclosure",
        "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=600&q=80",
        "material": "Rubberized Polymer & Fabric Mesh", "dimensions": "8.0 x 3.5 x 3.5 inches", "color": "Forest Green", "weight": "680g"
    },
    {
        "sku": "ELEC-CAM-004", "name": "ApexShot 4K Vlog Mirrorless Camera", "brand": "ApexShot",
        "category": "Electronics", "price": 799.00, "currency": "USD",
        "features": ["4K 60fps Uncropped Video", "Flip-out Touchscreen", "AI Eye Tracking AF", "Built-in Directional Mic"],
        "specifications": {"Sensor": "24.2MP APS-C CMOS", "ISO Range": "100-32000", "Mount": "E-Mount"},
        "target_audience": "Content creators, YouTubers, and travel photographers",
        "primary_keywords": ["4k vlogging camera", "mirrorless video camera"],
        "secondary_keywords": ["youtube camera", "autofocus vlog camera"],
        "usp": "Cinematic 4K clarity with intuitive eye-tracking autofocus",
        "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80",
        "material": "Polycarbonate body", "dimensions": "4.7 x 2.6 x 2.3 inches", "color": "Graphite Grey", "weight": "388g"
    },
    {
        "sku": "ELEC-MON-005", "name": "VisionPro 34-Inch Ultrawide Curved Monitor", "brand": "VisionPro",
        "category": "Electronics", "price": 499.99, "currency": "USD",
        "features": ["UWQHD 3440x1440 Resolution", "144Hz Refresh Rate", "1ms Response Time", "HDR400 Support"],
        "specifications": {"Curvature": "1500R", "Panel": "VA LED", "Ports": "2x HDMI 2.1, 1x DP 1.4"},
        "target_audience": "Gamers, video editors, and power productivity users",
        "primary_keywords": ["34 inch curved monitor", "ultrawide gaming monitor"],
        "secondary_keywords": ["144hz uwqhd screen", "curved display for work"],
        "usp": "Immersive 1500R curvature for panoramic focus and lag-free gaming",
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80",
        "material": "Aluminum stand", "dimensions": "31.8 x 18.2 x 9.4 inches", "color": "Matte Black", "weight": "7.8kg"
    },
    {
        "sku": "ELEC-BANK-006", "name": "VoltMax 25000mAh Laptop Power Bank", "brand": "VoltMax",
        "category": "Electronics", "price": 79.99, "currency": "USD",
        "features": ["100W USB-C Power Delivery", "TSA Approved Flight Capacity", "Smart LED Status Display", "Charge 3 Devices Simultaneously"],
        "specifications": {"Total Output": "145W", "Battery Cell": "Li-ion", "Inputs": "USB-C 65W fast recharge"},
        "target_audience": "Digital nomads, business travelers, and students",
        "primary_keywords": ["laptop power bank", "100w fast charging battery"],
        "secondary_keywords": ["high capacity portable charger", "usb c powerbank"],
        "usp": "Full-speed 100W MacBook charging in a flight-certified battery pack",
        "image_url": "https://images.unsplash.com/photo-1609592424074-8848b813f8aa?auto=format&fit=crop&w=600&q=80",
        "material": "Fireproof Anodized Aluminum", "dimensions": "6.2 x 3.1 x 1.0 inches", "color": "Space Grey", "weight": "490g"
    },
    {
        "sku": "ELEC-EAR-007", "name": "ClearTone Air True Wireless Earbuds", "brand": "ClearTone",
        "category": "Electronics", "price": 69.00, "currency": "USD",
        "features": ["Environmental Noise Cancellation Mic", "IPX5 Sweatproof", "Wireless Charging Case", "Low Latency Gaming Mode"],
        "specifications": {"Battery": "6 hours + 24 hours case", "Bluetooth": "5.3", "Codec": "AAC, SBC"},
        "target_audience": "Commuters, fitness enthusiasts, and casual listeners",
        "primary_keywords": ["true wireless earbuds", "bluetooth earbuds with mic"],
        "secondary_keywords": ["sweatproof wireless earphones", "affordable TWS buds"],
        "usp": "Crystal clear voice calls with ergonomic zero-pressure fit",
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=600&q=80",
        "material": "Polycarbonate", "dimensions": "2.2 x 1.8 x 0.9 inches", "color": "Pearl White", "weight": "45g"
    },
    {
        "sku": "ELEC-LAP-008", "name": "NovaBook Pro 15 Ultra Thin Laptop", "brand": "NovaBook",
        "category": "Electronics", "price": 1299.00, "currency": "USD",
        "features": ["Intel Core i7 13th Gen Processor", "16GB LPDDR5 RAM", "1TB NVMe Gen4 SSD", "15.6-inch OLED Touch Display"],
        "specifications": {"Resolution": "2880 x 1800", "Battery": "75Wh, 14 hours", "OS": "Windows 11 Pro"},
        "target_audience": "Software developers, creative professionals, and executives",
        "primary_keywords": ["ultra thin laptop", "oled touchscreen laptop"],
        "secondary_keywords": ["intel i7 business laptop", "lightweight 15 inch notebook"],
        "usp": "Stunning 2.8K OLED display paired with sleek 1.2kg ultrabook body",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80",
        "material": "CNC Aluminum Chassis", "dimensions": "14.1 x 9.2 x 0.59 inches", "color": "Starlight Silver", "weight": "1.25kg"
    },
    {
        "sku": "ELEC-TAB-009", "name": "OmniPad Air 11-Inch Stylus Tablet", "brand": "OmniPad",
        "category": "Electronics", "price": 499.00, "currency": "USD",
        "features": ["120Hz Liquid Motion Display", "4096 Levels Pressure Stylus Included", "Quad Speaker Stereo System", "WiFi 6E Connectivity"],
        "specifications": {"Storage": "256GB", "RAM": "8GB", "Processor": "Octa-Core 3.2GHz"},
        "target_audience": "Digital artists, students, and mobile professionals",
        "primary_keywords": ["stylus tablet for drawing", "11 inch 120hz tablet"],
        "secondary_keywords": ["android drawing tablet", "quad speaker tablet"],
        "usp": "Paper-like stylus writing response with 120Hz high refresh rate",
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=600&q=80",
        "material": "Anodized Aluminum", "dimensions": "9.8 x 6.5 x 0.24 inches", "color": "Space Black", "weight": "480g"
    },
    {
        "sku": "ELEC-KEY-010", "name": "TactilePro RGB Mechanical Gaming Keyboard", "brand": "TactilePro",
        "category": "Electronics", "price": 119.99, "currency": "USD",
        "features": ["Hot-Swappable Mechanical Switches", "Per-Key RGB Backlighting", "PBT Double-Shot Keycaps", "Detachable Braided Type-C Cable"],
        "specifications": {"Layout": "75% Compact", "Switch Type": "Gateron Yellow Linear", "Polling Rate": "1000Hz"},
        "target_audience": "Gamers, programmers, and mechanical keyboard enthusiasts",
        "primary_keywords": ["rgb mechanical keyboard", "hot swappable gaming keyboard"],
        "secondary_keywords": ["75 percent mechanical keyboard", "pbt keycaps keyboard"],
        "usp": "Smooth pre-lubed linear switches for creamy acoustics and rapid response",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80",
        "material": "PBT Plastics & Aluminum Plate", "dimensions": "12.8 x 5.5 x 1.4 inches", "color": "Retro White & Teal", "weight": "950g"
    },
    {
        "sku": "ELEC-MIC-011", "name": "VocalCraft Studio USB Condenser Microphone", "brand": "VocalCraft",
        "category": "Electronics", "price": 129.00, "currency": "USD",
        "features": ["24-bit / 96kHz High-Res Audio", "Cardioid & Omnidirectional Polar Patterns", "Zero-Latency Headphone Monitoring", "Touch Mute Sensor"],
        "specifications": {"Frequency Response": "20Hz - 20kHz", "Connection": "USB-C Plug & Play"},
        "target_audience": "Podcasters, streamers, voiceover artists, and remote workers",
        "primary_keywords": ["usb condenser microphone", "streaming podcast mic"],
        "secondary_keywords": ["studio quality usb mic", "cardioid microphone for pc"],
        "usp": "Broadcast-grade warmth and clarity with touch-sensitive instant mute",
        "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=600&q=80",
        "material": "Die-Cast Zinc Body", "dimensions": "8.5 x 3.8 x 3.8 inches", "color": "Matte Black", "weight": "710g"
    },
    {
        "sku": "ELEC-DRON-012", "name": "SkyHawk 4K GPS Mini Drone", "brand": "SkyHawk",
        "category": "Electronics", "price": 399.00, "currency": "USD",
        "features": ["Under 249g No FAA Registration Required", "3-Axis Gimbal 4K HDR Video", "30-Minute Flight Time", "10km HD Video Transmission"],
        "specifications": {"Max Speed": "16 m/s", "Obstacle Sensing": "Downward & Rear Sensors"},
        "target_audience": "Travelers, real estate videographers, and drone beginners",
        "primary_keywords": ["4k mini drone under 249g", "gps camera drone"],
        "secondary_keywords": ["3 axis gimbal drone", "portable folding drone"],
        "usp": "Ultra-portable folding drone delivering buttery smooth 4K videos without FAA hassle",
        "image_url": "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?auto=format&fit=crop&w=600&q=80",
        "material": "Lightweight Composite", "dimensions": "5.5 x 3.2 x 2.2 inches (Folded)", "color": "Arctic White", "weight": "242g"
    },
    {
        "sku": "ELEC-PROJ-013", "name": "CineBeam 1080P Smart Portable Projector", "brand": "CineBeam",
        "category": "Electronics", "price": 279.99, "currency": "USD",
        "features": ["Native 1080P Full HD with 4K Input Support", "Auto Focus & Auto Keystone Correction", "Built-In Android TV & Netflix", "Dual 5W Dolby Audio Speakers"],
        "specifications": {"Brightness": "500 ANSI Lumens", "Projection Size": "40 to 150 inches"},
        "target_audience": "Movie lovers, outdoor camping hosts, and gamers",
        "primary_keywords": ["portable smart projector", "1080p outdoor movie projector"],
        "secondary_keywords": ["autofocus mini projector", "android tv projector"],
        "usp": "Instant auto-focus rectangular projection on any wall or screen",
        "image_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=600&q=80",
        "material": "ABS Plastic & Fabric Mesh", "dimensions": "6.0 x 5.2 x 4.1 inches", "color": "Charcoal Grey", "weight": "1.1kg"
    },
    {
        "sku": "ELEC-VR-014", "name": "AuraVR Pro Wireless All-in-One VR Headset", "brand": "AuraVR",
        "category": "Electronics", "price": 449.00, "currency": "USD",
        "features": ["4K Dual LCD Display (2160x2160 Per Eye)", "Pass-Through Mixed Reality Color Cameras", "Hand Tracking & Ergonomic Touch Controllers", "Spatial 3D Audio"],
        "specifications": {"Refresh Rate": "120Hz", "Storage": "256GB", "Processor": "Snapdragon XR2 Gen 2"},
        "target_audience": "VR gamers, virtual meeting attendees, and tech enthusiasts",
        "primary_keywords": ["all in one vr headset", "mixed reality 4k headset"],
        "secondary_keywords": ["wireless gaming vr", "120hz virtual reality headset"],
        "usp": "Next-gen standalone mixed reality immersion without tether cables",
        "image_url": "https://images.unsplash.com/photo-1622979135225-d2ba269bc1bd?auto=format&fit=crop&w=600&q=80",
        "material": "Soft Fabric Strap & Polycarbonate Shell", "dimensions": "7.8 x 4.5 x 3.8 inches", "color": "Glacier White", "weight": "515g"
    },
    {
        "sku": "ELEC-SSD-015", "name": "VelocityExtreme 2TB Portable NVMe SSD", "brand": "VelocityExtreme",
        "category": "Electronics", "price": 169.99, "currency": "USD",
        "features": ["Up to 2000MB/s Read/Write Speed", "IP65 Water & Dust Resistance", "2-Meter Drop Protection", "256-bit AES Hardware Encryption"],
        "specifications": {"Interface": "USB 3.2 Gen 2x2", "Capacity": "2TB"},
        "target_audience": "4K video editors, photographers, gamers, and travelers",
        "primary_keywords": ["2tb portable nvme ssd", "fast external solid state drive"],
        "secondary_keywords": ["rugged waterproof ssd", "usb c external hard drive"],
        "usp": "Blazing fast 2000MB/s transfer speeds inside a drop-proof rubberized casing",
        "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=600&q=80",
        "material": "Silicon Rubber & Aluminum Core", "dimensions": "4.3 x 2.2 x 0.4 inches", "color": "Midnight Orange", "weight": "78g"
    },
    {
        "sku": "ELEC-ROUT-016", "name": "NetSpeed WiFi 7 Tri-Band Mesh Router System", "brand": "NetSpeed",
        "category": "Electronics", "price": 329.00, "currency": "USD",
        "features": ["WiFi 7 Multi-Link Operation (MLO)", "Speed Up to 11 Gbps Across 3 Bands", "Coverage Up to 6,000 Sq Ft", "10G Wideband Ethernet Port"],
        "specifications": {"Bands": "2.4GHz, 5GHz, 6GHz", "Supported Devices": "200+ Simultaneously"},
        "target_audience": "Smart homes, 4K/8K streamers, online gamers, and remote families",
        "primary_keywords": ["wifi 7 mesh router", "tri band home mesh system"],
        "secondary_keywords": ["gigabit wireless router", "high speed home network"],
        "usp": "Next-generation WiFi 7 technology delivering zero-lag gigabit coverage everywhere",
        "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=600&q=80",
        "material": "Satin Polycarbonate", "dimensions": "6.8 x 4.2 x 4.2 inches each", "color": "Pearl White", "weight": "820g"
    },
    {
        "sku": "ELEC-DASH-017", "name": "GuardDrive 4K Front and Rear Dash Cam", "brand": "GuardDrive",
        "category": "Electronics", "price": 159.50, "currency": "USD",
        "features": ["Real 4K Front + 1080P Rear Recording", "Sony STARVIS 2 Night Vision Sensor", "5GHz Wi-Fi & GPS Location Logging", "24/7 Parking Surveillance Mode"],
        "specifications": {"FOV": "170° Wide Angle Front, 140° Rear", "Screen": "3.0 inch IPS"},
        "target_audience": "Car owners, rideshare drivers, and daily commuters",
        "primary_keywords": ["4k front rear dash cam", "dual car security camera"],
        "secondary_keywords": ["sony starvis night vision dashcam", "parking monitor car cam"],
        "usp": "Ultra-clear 4K license plate recording day or night with instant phone app access",
        "image_url": "https://images.unsplash.com/photo-1508974239320-0a029497e820?auto=format&fit=crop&w=600&q=80",
        "material": "Heat Resistant ABS", "dimensions": "3.5 x 2.1 x 1.2 inches", "color": "Matte Black", "weight": "120g"
    },
    {
        "sku": "ELEC-HUB-018", "name": "SmartNest 10-Inch Touch Smart Home Hub", "brand": "SmartNest",
        "category": "Electronics", "price": 189.99, "currency": "USD",
        "features": ["10-Inch HD IPS Touchscreen", "Built-In Thread & Zigbee Smart Hub", "13MP Auto-Framing Video Call Camera", "Room-Filling Stereo Speakers"],
        "specifications": {"Resolution": "1280 x 800", "Microphones": "Far-field 3-mic array"},
        "target_audience": "Smart home enthusiasts, families, and seniors",
        "primary_keywords": ["smart home touch hub", "10 inch video call display"],
        "secondary_keywords": ["zigbee thread smart controller", "voice assistant display"],
        "usp": "Central control touch panel for all smart devices with auto-framing HD calls",
        "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=600&q=80",
        "material": "Fabric Base & Glass Display", "dimensions": "9.9 x 7.1 x 3.9 inches", "color": "Chalk Grey", "weight": "1.3kg"
    },
    {
        "sku": "ELEC-ACT-019", "name": "ActionPro 5K Waterproof Sports Cam", "brand": "ActionPro",
        "category": "Electronics", "price": 299.00, "currency": "USD",
        "features": ["5.3K 60fps & 4K 120fps Slow-Mo", "HyperSmooth 6.0 Image Stabilization", "Waterproof Up to 33ft (10m) Without Housing", "Dual Color LCD Screens"],
        "specifications": {"Sensor": "1/1.9\" CMOS", "Battery": "1900mAh Enduro Cold Weather"},
        "target_audience": "Surfers, skiers, mountain bikers, and extreme sports enthusiasts",
        "primary_keywords": ["5k waterproof action camera", "stabilized sports cam"],
        "secondary_keywords": ["4k 120fps slow mo camera", "dual screen action cam"],
        "usp": "Gimbal-like stabilization in a rugged camera built for freezing snow and ocean waves",
        "image_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=600&q=80",
        "material": "Rubberized Polycarbonate", "dimensions": "2.8 x 2.0 x 1.3 inches", "color": "Dark Graphite", "weight": "154g"
    },
    {
        "sku": "ELEC-RING-020", "name": "AuraRing Smart Sleep and Health Ring", "brand": "AuraRing",
        "category": "Electronics", "price": 249.00, "currency": "USD",
        "features": ["24/7 Heart Rate, HRV & Body Temp Sensing", "Sleep Stage Analytics & Readiness Score", "Lightweight Titanium Design", "7-Day Battery with Wireless Dock"],
        "specifications": {"Water Resistance": "100 Meters", "Material": "Grade 5 Titanium"},
        "target_audience": "Biohackers, wellness seekers, and runners who dislike wristwatches",
        "primary_keywords": ["smart ring health tracker", "titanium sleep tracking ring"],
        "secondary_keywords": ["hrv body temp wearable", "waterproof smart ring"],
        "usp": "Screenless health and sleep insights packed inside a sleek titanium ring",
        "image_url": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=600&q=80",
        "material": "Grade 5 Titanium & Biocompatible Inner Molding", "dimensions": "Sizes 6-13", "color": "Matte Silver", "weight": "4g"
    },
    {
        "sku": "ELEC-READ-021", "name": "PaperLite 7-Inch Waterproof E-Reader", "brand": "PaperLite",
        "category": "Electronics", "price": 139.99, "currency": "USD",
        "features": ["300 PPI Flush-Front E-Ink Carta Display", "Adjustable Warm White to Amber Reading Light", "IPX8 Waterproof for Bath & Pool Reading", "32GB Storage Holds 20,000+ Books"],
        "specifications": {"Battery": "Up to 10 Weeks", "Charging": "USB-C"},
        "target_audience": "Avid book readers, travelers, and nighttime readers",
        "primary_keywords": ["waterproof e-reader 300 ppi", "adjustable warm light ereader"],
        "secondary_keywords": ["e-ink digital book reader", "long battery life ereader"],
        "usp": "Glare-free paper reading experience in bright sunlight or pitch dark",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80",
        "material": "Soft-Touch Polycarbonate", "dimensions": "6.3 x 5.6 x 0.3 inches", "color": "Denim Blue", "weight": "205g"
    },
    {
        "sku": "ELEC-THER-022", "name": "EcoClimate Smart Learning Thermostat", "brand": "EcoClimate",
        "category": "Electronics", "price": 179.00, "currency": "USD",
        "features": ["Auto-Schedules Based on Household Habits", "Geofencing Auto-Away Energy Saver", "HVAC Monitoring & Maintenance Alerts", "Compatible with Alexa/Google/Apple Home"],
        "specifications": {"Screen": "2.1-inch Mirrored Glass Display", "Compatibility": "95% of 24V Systems"},
        "target_audience": "Homeowners seeking energy bill savings and remote temperature control",
        "primary_keywords": ["smart learning thermostat", "wifi programmable thermostat"],
        "secondary_keywords": ["energy saving smart thermostat", "geofencing hvac controller"],
        "usp": "Saves up to 15% on heating and 12% on cooling with automated schedule learning",
        "image_url": "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?auto=format&fit=crop&w=600&q=80",
        "material": "Polished Steel & Mirror Glass", "dimensions": "3.3 x 3.3 x 1.2 inches", "color": "Polished Brass", "weight": "260g"
    },
    {
        "sku": "ELEC-STUD-023", "name": "AudioPure 5-Inch Active Studio Monitors (Pair)", "brand": "AudioPure",
        "category": "Electronics", "price": 289.00, "currency": "USD",
        "features": ["5-Inch Kevlar Low-Frequency Driver", "1-Inch Silk Dome Tweeter", "Bi-Amplified 100W Class D Power", "Room Acoustic Tuning Controls"],
        "specifications": {"Frequency Range": "52Hz - 35kHz", "Inputs": "XLR, 1/4\" TRS, RCA"},
        "target_audience": "Music producers, sound engineers, content editors, and audiophiles",
        "primary_keywords": ["active studio monitors pair", "5 inch kevlar speaker monitors"],
        "secondary_keywords": ["music production speakers", "bi amplified studio monitors"],
        "usp": "Flat frequency response and surgical audio accuracy for music mixing",
        "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80",
        "material": "MDF Wooden Cabinet & Kevlar Cone", "dimensions": "11.2 x 7.0 x 9.5 inches each", "color": "Vinyl Black", "weight": "9.6kg pair"
    },
    {
        "sku": "ELEC-CHAR-024", "name": "MagTower 3-in-1 Foldable Magnetic Wireless Charger", "brand": "MagTower",
        "category": "Electronics", "price": 59.99, "currency": "USD",
        "features": ["Simultaneous Fast Charging for Phone, Smartwatch & Earbuds", "15W MagSafe Snap Alignment", "Foldable Travel Flat Design", "Smart Foreign Object Detection"],
        "specifications": {"Input": "USB-C 30W PD Required", "Output": "15W Phone + 5W Watch + 5W Buds"},
        "target_audience": "Frequent flyers, nightstand clutter clearers, and Apple/Android users",
        "primary_keywords": ["3 in 1 magsafe wireless charger", "foldable magnetic charging station"],
        "secondary_keywords": ["travel wireless charger stand", "fast charging nightstand dock"],
        "usp": "Folds flat like a wallet to eliminate desk wire clutter anywhere in the world",
        "image_url": "https://images.unsplash.com/photo-1622445268465-843d63286121?auto=format&fit=crop&w=600&q=80",
        "material": "Aluminum Alloy & Soft Silicone", "dimensions": "3.2 x 3.0 x 0.9 inches (Folded)", "color": "Space Grey", "weight": "195g"
    },
    {
        "sku": "ELEC-CHIP-025", "name": "QuantumDrive PCIe 5.0 4TB Gaming SSD", "brand": "QuantumDrive",
        "category": "Electronics", "price": 389.00, "currency": "USD",
        "features": ["Extreme Read Speeds Up to 14,000 MB/s", "Dedicated Aluminum Heatsink for Thermal Control", "DirectStorage Enabled for Instantly Loaded Games", "High Endurance 2400 TBW"],
        "specifications": {"Form Factor": "M.2 2280", "Interface": "NVMe PCIe Gen 5 x4"},
        "target_audience": "Hardcore PC gamers, 8K video editors, and AI workstations",
        "primary_keywords": ["pcie 5 0 nvme ssd 4tb", "14000 mb s gaming ssd"],
        "secondary_keywords": ["heatsink m2 ssd for pc", "fastest internal ssd drive"],
        "usp": "Breaks bandwidth records with 14,000 MB/s speeds for zero game load screens",
        "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=600&q=80",
        "material": "Anodized Black Aluminum Heatsink", "dimensions": "3.1 x 0.9 x 0.4 inches", "color": "Matte Black & Gold Accent", "weight": "45g"
    },

    # --- FASHION (25 Products) ---
    {
        "sku": "FASH-JACK-026", "name": "UrbanShield All-Weather Waterproof Jacket", "brand": "UrbanShield",
        "category": "Fashion", "price": 129.99, "currency": "USD",
        "features": ["3-Layer Breathable Membrane", "Seam-Sealed Zippers", "Adjustable Storm Hood", "Reflective Safety Trims"],
        "specifications": {"Waterproof Rating": "15,000mm", "Fit": "Regular Tailored", "Care": "Machine Wash Cold"},
        "target_audience": "Urban commuters, hikers, and outdoor enthusiasts",
        "primary_keywords": ["waterproof rain jacket", "breathable outdoor jacket"],
        "secondary_keywords": ["windbreaker jacket", "all weather coat"],
        "usp": "Ultimate storm protection paired with sleek urban aesthetics",
        "image_url": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=600&q=80",
        "material": "100% Recycled Ripstop Polyester", "dimensions": "Sizes S-XXL available", "color": "Charcoal Black", "weight": "450g"
    },
    {
        "sku": "FASH-SHOE-027", "name": "CloudStride Lightweight Running Shoes", "brand": "CloudStride",
        "category": "Fashion", "price": 110.00, "currency": "USD",
        "features": ["Responsive Nitrogen-Infused Foam", "Engineered Knit Mesh Upper", "High-Traction Rubber Outsole"],
        "specifications": {"Heel Drop": "8mm", "Arch Support": "Neutral", "Use": "Road Running & Gym"},
        "target_audience": "Marathon runners, daily joggers, and walkers",
        "primary_keywords": ["lightweight running shoes", "cushioned sneakers"],
        "secondary_keywords": ["breathable athletic shoes", "road running footwear"],
        "usp": "Cloud-like cushioning engineered for high-mileage endurance",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80",
        "material": "Flyknit Fabric & EVA Rubber", "dimensions": "US Mens 7-13", "color": "Electric Crimson", "weight": "230g"
    },
    {
        "sku": "FASH-DEN-028", "name": "HeritageFlex Slim Tapered Denim Jeans", "brand": "HeritageFlex",
        "category": "Fashion", "price": 79.50, "currency": "USD",
        "features": ["4-Way Comfort Stretch", "Classic 5-Pocket Styling", "Reinforced Stress Points", "Eco-Wash Technology"],
        "specifications": {"Rise": "Mid-Rise", "Leg Opening": "14 inches", "Inseam": "30, 32, 34"},
        "target_audience": "Modern men seeking stylish comfort for everyday wear",
        "primary_keywords": ["slim fit stretch jeans", "men tapered denim"],
        "secondary_keywords": ["comfortable blue jeans", "5 pocket flexible denim"],
        "usp": "Authentic denim look with 4-way stretch unrestricted freedom",
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=600&q=80",
        "material": "98% Organic Cotton, 2% Elastane", "dimensions": "Waist 28-40 inches", "color": "Vintage Indigo Wash", "weight": "580g"
    },
    {
        "sku": "FASH-SWEAT-029", "name": "CozyHaven Organic Fleece Hoodie", "brand": "CozyHaven",
        "category": "Fashion", "price": 59.99, "currency": "USD",
        "features": ["Double-Lined Hood with Drawstring", "Kangaroo Front Pocket", "Ribbed Cuffs and Hem", "Pre-Shrunk Fabric"],
        "specifications": {"Weight": "350 GSM Heavyweight", "Fit": "Relaxed Oversized"},
        "target_audience": "Loungewear lovers, college students, and casual wearers",
        "primary_keywords": ["organic cotton hoodie", "heavyweight fleece sweatshirt"],
        "secondary_keywords": ["cozy pullover hoodie", "relaxed fit sweater"],
        "usp": "Ultra-soft 350 GSM organic fleece built for lasting cozy warmth",
        "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=600&q=80",
        "material": "100% Organic French Terry Cotton", "dimensions": "Unisex XS-XXL", "color": "Oatmeal Heather", "weight": "620g"
    },
    {
        "sku": "FASH-SUN-030", "name": "SolStyle Polarized Aviator Sunglasses", "brand": "SolStyle",
        "category": "Fashion", "price": 45.00, "currency": "USD",
        "features": ["UV400 100% Sun Protection", "TAC Polarized Lenses", "Ultra-Lightweight Metal Frame", "Spring Hinges"],
        "specifications": {"Lens Width": "58mm", "Bridge": "14mm", "Temple Length": "138mm"},
        "target_audience": "Drivers, beach lovers, and fashion-forward individuals",
        "primary_keywords": ["polarized aviator sunglasses", "uv400 metal frame shades"],
        "secondary_keywords": ["driving sunglasses", "classic unisex eyewear"],
        "usp": "Glare-free optical precision wrapped in a timeless metal frame",
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=600&q=80",
        "material": "Monel Metal & TAC Lens", "dimensions": "Standard Adult", "color": "Gold Frame / Dark Green Lens", "weight": "28g"
    },
    {
        "sku": "FASH-BAG-031", "name": "LuxeLeather Minimalist Tote Handbag", "brand": "LuxeLeather",
        "category": "Fashion", "price": 185.00, "currency": "USD",
        "features": ["Padded Laptop Sleeve (Up to 15\")", "Magnetic Snap Closure", "Interior Zippered Valuables Pocket", "Gold-Plated Brass Hardware"],
        "specifications": {"Strap Drop": "10 inches", "Capacity": "16 Liters"},
        "target_audience": "Working professionals, executives, and stylish travelers",
        "primary_keywords": ["leather laptop tote bag", "women work handbag"],
        "secondary_keywords": ["minimalist tote", "genuine leather shoulder bag"],
        "usp": "Full-grain supple leather structured to carry laptops and work essentials with grace",
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=600&q=80",
        "material": "Full-Grain Cowhide Leather", "dimensions": "15.5 x 12.0 x 5.5 inches", "color": "Cognac Tan", "weight": "850g"
    },
    {
        "sku": "FASH-SOCK-032", "name": "ThermaWool Merino Hiking Socks (3-Pack)", "brand": "ThermaWool",
        "category": "Fashion", "price": 29.99, "currency": "USD",
        "features": ["Moisture-Wicking Merino Wool", "Targeted Heel & Toe Cushioning", "Arch Compression Support", "Seamless Toe Closure"],
        "specifications": {"Height": "Crew Sock", "Pack Size": "3 Pairs"},
        "target_audience": "Hikers, campers, winter walkers, and outdoor workers",
        "primary_keywords": ["merino wool hiking socks", "cushioned crew socks"],
        "secondary_keywords": ["anti blister socks", "warm moisture wicking socks"],
        "usp": "Blister-free thermal regulation that keeps feet dry in all seasons",
        "image_url": "https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?auto=format&fit=crop&w=600&q=80",
        "material": "70% Merino Wool, 25% Nylon, 5% Elastane", "dimensions": "Shoe Sizes 6-12", "color": "Olive / Charcoal / Navy", "weight": "180g"
    },
    {
        "sku": "FASH-BELT-033", "name": "CraftLeather Full Grain Italian Belt", "brand": "CraftLeather",
        "category": "Fashion", "price": 49.00, "currency": "USD",
        "features": ["100% Italian Full-Grain Vegetable Tanned Leather", "Solid Brass Brushed Buckle", "Single-Stitch Reinforced Edges", "Beveled Burnished Edges"],
        "specifications": {"Width": "1.4 inches (35mm)", "Sizing": "Waist 30-44 inches"},
        "target_audience": "Men seeking classic dress and casual belt durability",
        "primary_keywords": ["full grain leather belt", "italian dress leather belt"],
        "secondary_keywords": ["brass buckle belt", "casual men brown belt"],
        "usp": "Hand-burnished Italian leather that develops a magnificent personalized patina",
        "image_url": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?auto=format&fit=crop&w=600&q=80",
        "material": "Full-Grain Italian Leather & Brass", "dimensions": "1.4 inch width", "color": "Mahogany Brown", "weight": "190g"
    },
    {
        "sku": "FASH-TREN-034", "name": "VogueParis Double-Breasted Trench Coat", "brand": "VogueParis",
        "category": "Fashion", "price": 219.00, "currency": "USD",
        "features": ["Water-Resistant Cotton Twill", "Removable Waist Tie Belt", "Classic Epaulettes & Gun Flap", "Deep Storm Pockets"],
        "specifications": {"Length": "Mid-Calf", "Lining": "100% Satin Viscose"},
        "target_audience": "Fashion-conscious women, city commuters, and travelers",
        "primary_keywords": ["double breasted trench coat", "women waterproof trench"],
        "secondary_keywords": ["classic beige trench coat", "elegant belted spring coat"],
        "usp": "Timeless Parisian silhouette tailored in water-repellent gabardine twill",
        "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=600&q=80",
        "material": "100% Cotton Twill", "dimensions": "Sizes XS-XL", "color": "Classic Beige Honey", "weight": "920g"
    },
    {
        "sku": "FASH-SWEA-035", "name": "AlpineKnit Chunky Merino Wool Sweater", "brand": "AlpineKnit",
        "category": "Fashion", "price": 125.00, "currency": "USD",
        "features": ["100% Australian Extra-Fine Merino Wool", "Intricate Cable Knit Pattern", "Ribbed Crew Neckline & Cuffs", "Itch-Free Ultra Soft Feel"],
        "specifications": {"Knit Gauge": "Heavy 5-Gauge", "Fit": "Classic Tailored"},
        "target_audience": "Winter style seekers, cabin vacationers, and lovers of natural wool",
        "primary_keywords": ["chunky merino wool sweater", "men cable knit pullover"],
        "secondary_keywords": ["warm winter wool jumper", "itch free merino sweater"],
        "usp": "Heirloom cable knit warmth crafted from silky itch-free Australian merino",
        "image_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=600&q=80",
        "material": "100% Merino Wool", "dimensions": "Men's S-XXL", "color": "Cream Ivory", "weight": "680g"
    },
    {
        "sku": "FASH-LOAF-036", "name": "MilanoCraft Leather Penny Loafers", "brand": "MilanoCraft",
        "category": "Fashion", "price": 159.00, "currency": "USD",
        "features": ["Hand-Burnished Calfskin Leather Upper", "Goodyear Welted Leather Outsole", "Memory Foam Padded Insole", "Classic Saddle Strap Detail"],
        "specifications": {"Construction": "Goodyear Welted", "Closure": "Slip-On"},
        "target_audience": "Business professionals, smart-casual dressers, and wedding guests",
        "primary_keywords": ["men leather penny loafers", "handcrafted dress loafers"],
        "secondary_keywords": ["goodyear welted slip on shoes", "calfskin leather footwear"],
        "usp": "Hand-stitched Goodyear welted calfskin that offers custom ergonomic comfort over time",
        "image_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=600&q=80",
        "material": "Calfskin Leather & Leather Sole", "dimensions": "US Mens 7-13", "color": "Burnished Dark Walnut", "weight": "440g"
    },
    {
        "sku": "FASH-SCAR-037", "name": "SilkFlora Hand-Printed 100% Silk Scarf", "brand": "SilkFlora",
        "category": "Fashion", "price": 68.00, "currency": "USD",
        "features": ["100% Pure Mulberry Silk (16 Momme)", "Hand-Rolled Hem Edges", "Vibrant Botanical Watercolor Print", "Hypoallergenic & Gentle on Hair"],
        "specifications": {"Dimensions": "35 x 35 inches (90x90cm Square)"},
        "target_audience": "Stylish women, luxury accessory gift buyers, and art lovers",
        "primary_keywords": ["pure mulberry silk scarf", "hand printed botanical silk square"],
        "secondary_keywords": ["luxury head scarf silk", "hand rolled hem silk shawl"],
        "usp": "Lustrous 16-momme mulberry silk with hand-rolled hems and original hand-painted artwork",
        "image_url": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?auto=format&fit=crop&w=600&q=80",
        "material": "100% Mulberry Silk", "dimensions": "35.0 x 35.0 inches", "color": "Emerald & Blush Floral", "weight": "65g"
    },
    {
        "sku": "FASH-SHORT-038", "name": "VelocityPro 7-Inch Athletic Running Shorts", "brand": "VelocityPro",
        "category": "Fashion", "price": 42.00, "currency": "USD",
        "features": ["Lightweight 4-Way Stretch Fabric", "Built-In Anti-Chafing Compression Liner", "Zippered Phone Pocket on Hip", "Laser-Cut Breathable Vent Holes"],
        "specifications": {"Inseam": "7 inches", "Waist": "Elastic with Internal Drawcord"},
        "target_audience": "Marathoners, gym enthusiasts, and Crossfit runners",
        "primary_keywords": ["running shorts with phone pocket", "men athletic shorts with liner"],
        "secondary_keywords": ["anti chafing workout shorts", "lightweight 7 inch shorts"],
        "usp": "Zero-bounce phone pocket inside a silky anti-chafing compression liner",
        "image_url": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?auto=format&fit=crop&w=600&q=80",
        "material": "88% Polyester, 12% Spandex", "dimensions": "Men S-XL", "color": "Slate Grey & Neon Yellow Accent", "weight": "165g"
    },
    {
        "sku": "FASH-BLAZ-039", "name": "SavileRow Italian Wool Unstructured Blazer", "brand": "SavileRow",
        "category": "Fashion", "price": 279.00, "currency": "USD",
        "features": ["Super 120s Italian Hopsack Wool", "Unstructured Soft Shoulder Tailoring", "Patch Pockets & Dual Back Vents", "Half-Lined for Breathable Layering"],
        "specifications": {"Fit": "Modern Slim Fit", "Care": "Dry Clean Only"},
        "target_audience": "Modern businessmen, smart-casual wedding goers, and travelers",
        "primary_keywords": ["unstructured wool blazer", "italian hopsack sport coat"],
        "secondary_keywords": ["men slim fit blazer", "breathable navy dress jacket"],
        "usp": "Lightweight unstructured drape made from breathable Super 120s Italian wool",
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=600&q=80",
        "material": "100% Italian Wool", "dimensions": "Sizes 36R-46R", "color": "Deep Navy Blue", "weight": "650g"
    },
    {
        "sku": "FASH-BOOT-040", "name": "TerraTrek Waterproof Leather Chelsea Boots", "brand": "TerraTrek",
        "category": "Fashion", "price": 169.99, "currency": "USD",
        "features": ["Waterproof Full-Grain Oiled Leather", "Elastic Side Gore Panels for Easy Slip-On", "Vibram High-Traction Rubber Lug Sole", "Anti-Fatigue Removable Footbed"],
        "specifications": {"Shaft Height": "5.5 inches", "Sole": "Vibram Rubber"},
        "target_audience": "Urban explorers, commuters in wet weather, and stylish workers",
        "primary_keywords": ["waterproof leather chelsea boots", "men rubber lug sole boots"],
        "secondary_keywords": ["vibram sole chelsea boot", "slip on leather work boot"],
        "usp": "Rugged Vibram mountain grip hidden beneath a sleek waterproof Chelsea silhouette",
        "image_url": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?auto=format&fit=crop&w=600&q=80",
        "material": "Oiled Full-Grain Leather & Vibram Rubber", "dimensions": "US Mens 7-13", "color": "Dark Espresso Brown", "weight": "680g"
    },
    {
        "sku": "FASH-PUFF-041", "name": "EcoLoft 700-Fill Recycled Down Puffer Vest", "brand": "EcoLoft",
        "category": "Fashion", "price": 99.00, "currency": "USD",
        "features": ["700-Fill Power Responsible Down Standard", "DWR Durable Water Repellent Finish", "Packable into Internal Pocket", "Fleece-Lined Handwarmer Pockets"],
        "specifications": {"Weight": "280g Lightweight", "Insulation": "90/10 Down Feather"},
        "target_audience": "Hikers, commuters, campers, and fall/winter layermen",
        "primary_keywords": ["700 fill down puffer vest", "packable lightweight vest"],
        "secondary_keywords": ["water resistant down gilet", "recycled outerwear vest"],
        "usp": "Ultra-warm 700-fill down that compresses smaller than a water bottle",
        "image_url": "https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=600&q=80",
        "material": "100% Recycled Ripstop Nylon", "dimensions": "Men S-XXL", "color": "Matte Forest Olive", "weight": "280g"
    },
    {
        "sku": "FASH-BEAN-042", "name": "NordicWarm Merino Ribbed Beanie Hat", "brand": "NordicWarm",
        "category": "Fashion", "price": 28.00, "currency": "USD",
        "features": ["100% Pure Extra-Fine Merino Wool", "Fold-Over Adjustable Cuff", "Seamless Circular Knit Construction", "Naturally Odor-Resistant"],
        "specifications": {"Sizing": "One Size Fits Most", "Weight": "70g"},
        "target_audience": "Skiers, winter commuters, and casual streetwear dressers",
        "primary_keywords": ["merino wool ribbed beanie", "warm winter watch hat"],
        "secondary_keywords": ["cuffed merino knit cap", "itchless soft beanie"],
        "usp": "Zero-itch pure merino wool delivering breathable warmth in a classic ribbed cuff style",
        "image_url": "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?auto=format&fit=crop&w=600&q=80",
        "material": "100% Merino Wool", "dimensions": "Unisex One Size", "color": "Charcoal Heather", "weight": "70g"
    },
    {
        "sku": "FASH-TEE-043", "name": "PureCotton Heavyweight 280 GSM Oversized Tee", "brand": "PureCotton",
        "category": "Fashion", "price": 35.00, "currency": "USD",
        "features": ["280 GSM Premium Combed Cotton", "Drop Shoulder Boxy Streetwear Cut", "Thick 1-Inch Ribbed Collar", "Pre-Shrunk Organic Cotton"],
        "specifications": {"Fit": "Boxy Oversized", "Fabric Weight": "8.2 oz Heavyweight"},
        "target_audience": "Streetwear lovers, skaters, and casual fashion dressers",
        "primary_keywords": ["heavyweight 280 gsm t shirt", "oversized boxy cotton tee"],
        "secondary_keywords": ["thick collar streetwear t-shirt", "drop shoulder plain tee"],
        "usp": "Substantial 280 GSM combed cotton that holds its boxy streetwear shape wash after wash",
        "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=600&q=80",
        "material": "100% Organic Combed Cotton", "dimensions": "Unisex S-XL", "color": "Washed Vintage Black", "weight": "310g"
    },
    {
        "sku": "FASH-CHIN-044", "name": "FlexChino Stretch Athletic-Fit Pants", "brand": "FlexChino",
        "category": "Fashion", "price": 69.50, "currency": "USD",
        "features": ["3% Spandex Flex Stretch", "Roomy Thighs with Tapered Ankle", "Wrinkle-Resistant Easy Care", "Hidden Zipper Security Pocket"],
        "specifications": {"Rise": "Mid-Rise", "Leg Opening": "13.5 inches"},
        "target_audience": "Men with athletic legs, office workers, and golf players",
        "primary_keywords": ["athletic fit stretch chinos", "men wrinkle resistant pants"],
        "secondary_keywords": ["tapered casual dress trousers", "comfortable flex chinos"],
        "usp": "Tailored for athletic thighs with 4-way stretch mobility for work and weekends",
        "image_url": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=600&q=80",
        "material": "97% Cotton, 3% Spandex", "dimensions": "Waist 30-40 in", "color": "British Tan Khaki", "weight": "460g"
    },
    {
        "sku": "FASH-GLOV-045", "name": "WarmTouch Touchscreen Genuine Leather Gloves", "brand": "WarmTouch",
        "category": "Fashion", "price": 48.00, "currency": "USD",
        "features": ["Precision Touchscreen Compatibility on All 10 Fingers", "100% Supple Sheepskin Nappa Leather", "100% Pure Cashmere Thermal Lining", "Elasticized Snug Wrist Cuff"],
        "specifications": {"Lining": "100% Soft Cashmere", "Sizing": "Men & Women S-XL"},
        "target_audience": "Winter commuters, smartphone users, and drivers",
        "primary_keywords": ["touchscreen leather gloves", "cashmere lined sheepskin gloves"],
        "secondary_keywords": ["winter driving gloves men women", "warm phone leather gloves"],
        "usp": "Ultra-soft cashmere warmth with 10-finger capacitive phone touchscreen control",
        "image_url": "https://images.unsplash.com/photo-1516762689617-e1cffcef479d?auto=format&fit=crop&w=600&q=80",
        "material": "Sheepskin Leather & Cashmere", "dimensions": "Standard S-XL", "color": "Onyx Black", "weight": "110g"
    },
    {
        "sku": "FASH-SWIM-046", "name": "AquaFlex Quick-Dry 5-Inch Swim Trunks", "brand": "AquaFlex",
        "category": "Fashion", "price": 45.00, "currency": "USD",
        "features": ["Ultra Fast 3-Minute Quick Dry Fabric", "Silky Smooth Built-in Mesh Compression Liner", "Water-Repellent UPF 50+ Sun Protection", "Key Loop & Zippered Back Pocket"],
        "specifications": {"Inseam": "5 inches", "Sun Rating": "UPF 50+"},
        "target_audience": "Beachgoers, swimmers, vacationers, and pool party hosts",
        "primary_keywords": ["5 inch quick dry swim trunks", "men upf 50 swim shorts"],
        "secondary_keywords": ["compression liner beach shorts", "fast drying board shorts"],
        "usp": "Dries in under 3 minutes with a buttery soft anti-chafing inner liner",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80",
        "material": "90% Recycled Polyester, 10% Elastane", "dimensions": "Men S-XXL", "color": "Coral Red Palm Print", "weight": "170g"
    },
    {
        "sku": "FASH-DENJ-047", "name": "HeritageVintage Sherpa-Lined Denim Trucker Jacket", "brand": "HeritageVintage",
        "category": "Fashion", "price": 119.00, "currency": "USD",
        "features": ["13.5 oz Heavyweight Cotton Denim", "Plush Warm Sherpa Fleece Lining", "Quilted Smooth Sleeve Lining", "Adjustable Waist Tabs & Metal Snap Buttons"],
        "specifications": {"Weight": "13.5 oz Raw Denim", "Fit": "Classic Regular"},
        "target_audience": "Casual style lovers, outdoor casual dressers, and denim fans",
        "primary_keywords": ["sherpa lined denim jacket", "men fleece trucker jacket"],
        "secondary_keywords": ["warm winter jean jacket", "heavyweight vintage denim coat"],
        "usp": "Rugged 13.5oz vintage denim insulated with thick cloud-soft sherpa fleece",
        "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=600&q=80",
        "material": "100% Cotton Denim & Polyester Sherpa", "dimensions": "Men S-XXL", "color": "Washed Stonewash Blue", "weight": "1.1kg"
    },
    {
        "sku": "FASH-ANKL-048", "name": "SuedeStyle Block Heel Ankle Bootie", "brand": "SuedeStyle",
        "category": "Fashion", "price": 139.00, "currency": "USD",
        "features": ["Water-Resistant Genuine Suede Upper", "Comfortable 2.5-Inch Stacked Block Heel", "Side Zipper for Quick On/Off", "Cushioned OrthoLite Memory Foam Insole"],
        "specifications": {"Heel Height": "2.5 inches", "Shaft": "4.5 inches"},
        "target_audience": "Women dressers, office workers, and autumn fashion lovers",
        "primary_keywords": ["women suede ankle booties", "stacked block heel boots"],
        "secondary_keywords": ["comfortable suede dress boots", "water resistant women booties"],
        "usp": "All-day walkable 2.5-inch block heel combined with water-resistant velvet suede",
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=600&q=80",
        "material": "Genuine Calf Suede & Rubber Sole", "dimensions": "US Women 5-11", "color": "Taupe Sand", "weight": "420g"
    },
    {
        "sku": "FASH-PANT-049", "name": "LuxeLounge Bamboo Cashmere Jogger Pants", "brand": "LuxeLounge",
        "category": "Fashion", "price": 75.00, "currency": "USD",
        "features": ["Silky Soft Bamboo Fiber + Cashmere Blend", "Thermal Temperature Regulating", "Elastic Waistband with Metal Tipped Drawstring", "Deep Tapered Side Pockets"],
        "specifications": {"Blend": "70% Bamboo Viscose, 25% Cotton, 5% Cashmere"},
        "target_audience": "Work-from-home workers, travelers, and luxury loungewear seekers",
        "primary_keywords": ["bamboo cashmere jogger pants", "luxury soft sweatpants"],
        "secondary_keywords": ["breathable travel lounge pants", "tapered bamboo joggers"],
        "usp": "Unrivaled silky softness that regulates temperature during travel or lounging",
        "image_url": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?auto=format&fit=crop&w=600&q=80",
        "material": "70% Bamboo Viscose, 25% Cotton, 5% Cashmere", "dimensions": "Unisex S-XL", "color": "Heather Heather Grey", "weight": "380g"
    },
    {
        "sku": "FASH-HAT-050", "name": "PanamaCraft Handwoven Fedora Straw Hat", "brand": "PanamaCraft",
        "category": "Fashion", "price": 85.00, "currency": "USD",
        "features": ["100% Handwoven Ecuadorian Toquilla Straw", "UPF 50+ Sun Protection Brim", "Interior Moisture-Wicking Sweatband", "Classic Black Grosgrain Ribbon Band"],
        "specifications": {"Brim Width": "2.75 inches", "Grade": "Brisa Weave Grade 8"},
        "target_audience": "Resort travelers, summer fashion lovers, and beachgoers",
        "primary_keywords": ["handwoven panama straw hat", "upf 50 fedora sun hat"],
        "secondary_keywords": ["ecuadorian straw fedora", "resort summer straw hat"],
        "usp": "Genuine handwoven Ecuadorian Toquilla straw offering breathable UPF 50+ shade",
        "image_url": "https://images.unsplash.com/photo-1514327605112-b887c0e61c0a?auto=format&fit=crop&w=600&q=80",
        "material": "100% Toquilla Straw", "dimensions": "Brim 2.75 in", "color": "Natural Bleached Straw", "weight": "110g"
    }
]

# Add Home & Kitchen (15 items), Beauty (12 items), Sports (12 items), Grocery (10 items), Furniture (10 items), Travel (11 items)
# to reach 113 TOTAL products!

extra_categories = [
    # HOME & KITCHEN (15 items)
    ("HOME-COFF-051", "BaristaCraft Espresso Machine", "BaristaCraft", "Home and Kitchen", 349.99, ["15-Bar Italian Pump", "Burr Grinder", "PID Control"], "Café quality espresso"),
    ("HOME-AIR-052", "CrispChef Dual Zone Air Fryer", "CrispChef", "Home and Kitchen", 139.99, ["Dual Independent Baskets", "8 Presets"], "Cook 2 foods 2 ways simultaneously"),
    ("HOME-KNIF-053", "PrecisionBlade 8-inch Damascus Knife", "PrecisionBlade", "Home and Kitchen", 85.00, ["67 Layer Damascus Steel", "VG10 Core"], "Effortless precision slicing"),
    ("HOME-ROBO-054", "CleanSweep X10 Robot Vacuum", "CleanSweep", "Home and Kitchen", 429.00, ["LiDAR 3D Mapping", "4000Pa Suction", "Self Empty"], "Hands-free floor cleaning for 60 days"),
    ("HOME-PAN-055", "IronChef 12-inch Cast Iron Skillet", "IronChef", "Home and Kitchen", 38.99, ["Pre-seasoned Natural Oil", "Oven Safe 500F"], "Heirloom durability for perfect searing"),
    ("HOME-BLEN-056", "NutriBlend Max 1200W Blender", "NutriBlend", "Home and Kitchen", 99.99, ["1200W Peak Motor", "Extractor Blades"], "Pulverizes ice and greens in 30 seconds"),
    ("HOME-SET-057", "PureLinen 100% French Flax Sheet Set", "PureLinen", "Home and Kitchen", 165.00, ["100% French Flax", "Thermoregulating"], "Breathable vintage softness wash after wash"),
    ("HOME-POT-058", "ChefMaster 6-Quart Enamel Dutch Oven", "ChefMaster", "Home and Kitchen", 89.99, ["Heavy Enameled Cast Iron", "Self-Basting Lid"], "Superior heat retention for slow roasts"),
    ("HOME-VAC-059", "CyclonePro Cordless Stick Vacuum", "CyclonePro", "Home and Kitchen", 219.00, ["250W Brushless Motor", "45 Min Run Time"], "Ultra lightweight 1.5kg cordless suction"),
    ("HOME-MUG-060", "TempGuard Smart Heated Travel Mug", "TempGuard", "Home and Kitchen", 119.00, ["App Temperature Control 120F-145F", "3 Hr Battery"], "Keeps coffee at your exact preferred temp"),
    ("HOME-JUIC-061", "VitalJuice Cold Press Masticating Juicer", "VitalJuice", "Home and Kitchen", 149.00, ["Slow 80 RPM Masticating Auger", "Quiet Motor"], "Yields 30% more juice with minimal oxidation"),
    ("HOME-KEG-062", "HydroDraft Carbonated Growler 64oz", "HydroDraft", "Home and Kitchen", 99.00, ["CO2 Carbonation Tap", "Vacuum Insulated"], "Keeps draft beer fresh and fizzy for 2 weeks"),
    ("HOME-KETT-063", "PrecisionPour Gooseneck Electric Kettle", "PrecisionPour", "Home and Kitchen", 79.99, ["1-Degree Temp Control", "Gooseneck Spout"], "Perfect pour-over water stream control"),
    ("HOME-BOWL-064", "ArtisanCeramics Handcrafted Bowl Set (4-Pack)", "ArtisanCeramics", "Home and Kitchen", 45.00, ["Stoneware Reactive Glaze", "Microwave Dishwasher Safe"], "Unique hand-painted stoneware glazes"),
    ("HOME-ORGAN-065", "BambooChef Expandable Spice Rack", "BambooChef", "Home and Kitchen", 29.99, ["Sustainable Moso Bamboo", "3 Tier Step Display"], "Organizes up to 30 spice jars neatly"),

    # BEAUTY AND PERSONAL CARE (12 items)
    ("BEAU-SERU-066", "RadiantGlow Vitamin C + Ferulic Serum", "RadiantGlow", "Beauty and Personal Care", 48.00, ["15% L-Ascorbic Acid", "Hyaluronic Acid"], "Brightens dark spots in 14 days"),
    ("BEAU-DRY-067", "SilkBlow Ionic Salon Hair Dryer", "SilkBlow", "Beauty and Personal Care", 119.00, ["110k RPM Brushless Motor", "Ionic Frizz Control"], "Dries hair 2x faster without heat damage"),
    ("BEAU-CREA-068", "HydroPlump Ceramide Moisture Cream", "HydroPlump", "Beauty and Personal Care", 42.50, ["5 Essential Ceramides", "Peptide Matrix"], "24-hour deep skin barrier repair"),
    ("BEAU-BRUS-069", "SonicGleam Pro Electric Toothbrush", "SonicGleam", "Beauty and Personal Care", 64.99, ["48,000 VPM Motor", "5 Custom Modes"], "Removes 10x more plaque than manual brush"),
    ("BEAU-SUN-070", "SunGuard Mineral Sunscreen SPF 50", "SunGuard", "Beauty and Personal Care", 28.00, ["100% Non-Nano Zinc", "Zero White Cast"], "Clear broad-spectrum reef-safe sun protection"),
    ("BEAU-PERF-071", "VelvetOud Eau De Parfum Spray 100ml", "VelvetOud", "Beauty and Personal Care", 95.00, ["Cambodian Oud & Amberwood", "12 Hr Projection"], "Exotic luxurious fragrance trail"),
    ("BEAU-MASK-072", "GlowLED 7-Color Light Therapy Face Mask", "GlowLED", "Beauty and Personal Care", 149.00, ["Medical Grade LED Diodes", "Red/Blue/Near-IR"], "Stimulates collagen & reduces acne at home"),
    ("BEAU-OIL-073", "ArganLux 100% Pure Moroccan Argan Oil", "ArganLux", "Beauty and Personal Care", 24.00, ["Cold Pressed Organic Argan", "Hair & Skin"], "Deep nourishing shine for dry hair & cuticles"),
    ("BEAU-LIP-074", "VelvetMatte Liquid Lip Color Trio", "VelvetMatte", "Beauty and Personal Care", 36.00, ["16-Hour Transfer Proof", "Hydrating Vitamin E"], "Weightless matte color that lasts all day"),
    ("BEAU-SCAL-075", "ScalpTherapy Sonic Massager Brush", "ScalpTherapy", "Beauty and Personal Care", 32.00, ["Red Light LED + Sonic Vibration", "Waterproof"], "Promotes hair growth & relieves scalp tension"),
    ("BEAU-SHAV-076", "BarberPrecision Cordless Foil Shaver", "BarberPrecision", "Beauty and Personal Care", 89.00, ["Hypoallergenic Titanium Foil", "9000 RPM Motor"], "Ultra-close zero-gap shave without razor bumps"),
    ("BEAU-EYE-077", "YouthEye Peptide Recovery Eye Cream", "YouthEye", "Beauty and Personal Care", 38.00, ["Caffeine + Niacinamide", "Cooling Metal Tip"], "Reduces dark circles & puffy under-eye bags"),

    # SPORTS AND FITNESS (12 items)
    ("SPOR-MAT-078", "ZenMat Extra Thick Non-Slip Yoga Mat", "ZenMat", "Sports and Fitness", 45.00, ["6mm TPE Foam", "Laser Alignment Lines"], "Joint cushioning with precision alignment"),
    ("SPOR-DUMB-079", "FlexBell 50 lb Adjustable Dumbbells", "FlexBell", "Sports and Fitness", 299.99, ["5-50 lb Dial Adjustment", "Compact Storage"], "Replaces 10 pairs of weights in one dial"),
    ("SPOR-BOTT-080", "HydroFlow 32oz Insulated Water Bottle", "HydroFlow", "Sports and Fitness", 32.99, ["Double Wall Vacuum", "24 Hr Cold"], "Sweat-free icy hydration all day"),
    ("SPOR-BAND-081", "PowerFlex Heavy Duty Resistance Bands", "PowerFlex", "Sports and Fitness", 24.95, ["5 Latex Levels", "Handles & Door Anchor"], "Versatile full body workout anywhere"),
    ("SPOR-BIKE-082", "VelocityPro Magnetic Spin Bike", "VelocityPro", "Sports and Fitness", 449.00, ["35 lb Flywheel", "Magnetic Resistance"], "Whisper quiet indoor studio cycling"),
    ("SPOR-ROPE-083", "SpeedBurn Pro Bearing Jump Rope", "SpeedBurn", "Sports and Fitness", 18.99, ["360 Swivel Ball Bearings", "Adjustable Steel Cable"], "Frictionless double-unders speed jump rope"),
    ("SPOR-ROLLER-084", "DeepRelief Vibration Foam Roller", "DeepRelief", "Sports and Fitness", 69.99, ["4 Intensity Vibration Speeds", "High Density Grid"], "Accelerates muscle recovery & flushes soreness"),
    ("SPOR-BENCH-085", "IronGrip Heavy-Duty Adjustable Weight Bench", "IronGrip", "Sports and Fitness", 159.00, ["800 lb Capacity", "7 Backrest Incline Angles"], "Commercial grade steel bench for home workouts"),
    ("SPOR-GLOV-086", "ProStrike 16oz Gel Boxing Gloves", "ProStrike", "Sports and Fitness", 59.00, ["Multi-Layer Gel Padding", "Breathable Mesh Palm"], "Maximum knuckle protection for heavy bag training"),
    ("SPOR-TENT-087", "AlpinePeak 4-Person Waterproof Camping Tent", "AlpinePeak", "Sports and Fitness", 139.00, ["3000mm Rainfly Coating", "5-Minute Setup"], "Weatherproof shelter for outdoor weekend camping"),
    ("SPOR-PADD-088", "AquaGlide Inflatable Stand-Up Paddleboard", "AquaGlide", "Sports and Fitness", 329.00, ["6-Inch Drop Stitch PVC", "Dual Action Pump & Paddle"], "Ultra stable paddleboard bundle with backpack"),
    ("SPOR-GUN-089", "PulseRelief Deep Tissue Massage Gun", "PulseRelief", "Sports and Fitness", 89.00, ["Brushless High Torque Motor", "6 Attachment Heads"], "12mm amplitude percussive muscle therapy"),

    # GROCERY (10 items)
    ("GROC-COFF-090", "Organic Peak Arabica Whole Bean Coffee 2 lb", "Organic Peak", "Grocery", 24.99, ["100% Fair Trade Organic", "Medium Dark Roast"], "Single origin Ethiopian aromatic dark roast"),
    ("GROC-OIL-091", "TuscanGold Extra Virgin Olive Oil 1L", "TuscanGold", "Grocery", 21.50, ["First Cold Pressed", "Acidity < 0.3%"], "Fresh peppery early harvest estate olive oil"),
    ("GROC-HON-092", "NatureBee Raw Wildflower Honey 24oz", "NatureBee", "Grocery", 16.99, ["100% Raw & Unfiltered", "Natural Pollen"], "Untouched natural wildflower hive honey"),
    ("GROC-TEA-093", "ZenMatcha Ceremonial Grade Powder 100g", "ZenMatcha", "Grocery", 29.99, ["First Harvest Spring Leaves", "Uji Kyoto Japan"], "Vibrant green umami matcha without bitterness"),
    ("GROC-OAT-094", "PureHarvest Gluten Free Organic Rolled Oats 3 lb", "PureHarvest", "Grocery", 12.99, ["Certified Gluten-Free", "Whole Grain Thick Cut"], "Creamy thick-cut overnight oatmeal staple"),
    ("GROC-CHO-095", "CocoaCraft 85% Single Origin Dark Chocolate (6-Pack)", "CocoaCraft", "Grocery", 22.00, ["85% Ecuadorian Organic Cacao", "Fair Trade Certified"], "Rich antioxidant rich dark chocolate bars"),
    ("GROC-NUT-096", "NaturaNuts Raw Organic Macadamia Nuts 1 lb", "NaturaNuts", "Grocery", 19.99, ["Whole Style 1 Raw Macadamias", "Unsalted"], "Rich buttery keto friendly raw macadamia nuts"),
    ("GROC-SALT-097", "HimalayanPure Pink Coarse Salt Grinder 1.5 lb", "HimalayanPure", "Grocery", 14.50, ["100% Natural Pink Mineral Salt", "Ceramic Grinder"], "84 trace minerals in natural pink crystal salt"),
    ("GROC-MAPL-098", "VermontGold Grade A Amber Maple Syrup 32oz", "VermontGold", "Grocery", 23.99, ["100% Pure Vermont Maple", "Rich Amber Taste"], "Traditional wood-fired maple syrup jug"),
    ("GROC-CHIA-099", "SuperSeed Organic Black Chia Seeds 2 lb", "SuperSeed", "Grocery", 11.99, ["Raw Non-GMO Black Chia", "High Omega-3 & Fiber"], "Nutrient-dense superfood for smoothies & puddings"),

    # FURNITURE (10 items)
    ("FURN-CHAI-100", "ErgoFlex Mesh High-Back Office Chair", "ErgoFlex", "Furniture", 249.99, ["2D Dynamic Lumbar", "3D Armrests", "Breathable Mesh"], "Ergonomic support for 10-hour workdays"),
    ("FURN-DESK-101", "ModuDesk Motorized Electric Standing Desk 55\"", "ModuDesk", "Furniture", 399.00, ["Dual Motor Elevation", "4 Memory Presets", "Walnut Top"], "Smooth sit-stand transitions for healthy work"),
    ("FURN-SOFA-102", "HavenNordic 3-Seater Velvet Sofa", "HavenNordic", "Furniture", 699.00, ["Stain-Resistant Velvet", "Hardwood Frame"], "Mid-century Scandinavian velvet couch"),
    ("FURN-BOOK-103", "CraftWood 5-Tier Industrial Bookshelf", "CraftWood", "Furniture", 149.50, ["Thick Rustic Oak Shelves", "Steel X-Brace Frame"], "Rugged steel framing with rustic wood shelves"),
    ("FURN-LAMP-104", "LuminaArc Dimmable Modern Floor Lamp", "LuminaArc", "Furniture", 89.99, ["Overarching Arc Design", "Weighted Marble Base"], "Dramatic sweeping overhead reading light"),
    ("FURN-TABL-105", "UrbanNest Extendable Dining Table", "UrbanNest", "Furniture", 529.00, ["Hidden Butterfly Leaf", "Solid Oak Finish"], "Expands from 6 to 8 seats in 15 seconds"),
    ("FURN-BED-106", "NordicRest Solid Walnut Platform Bed (Queen)", "NordicRest", "Furniture", 599.00, ["100% Solid American Walnut", "Wooden Slat Support"], "Minimalist Japanese modern platform bed frame"),
    ("FURN-SIDE-107", "RetroGrain Mid-Century Nightstand Table", "RetroGrain", "Furniture", 119.00, ["Solid Rubberwood", "Dovetail Drawer"], "Warm retro wood nightstand with cable slot"),
    ("FURN-CAB-108", "ModernArt 4-Door Sideboard Credenza", "ModernArt", "Furniture", 449.00, ["Fluted Wood Panel Doors", "Adjustable Shelving"], "Elegant entryway storage & media credenza"),
    ("FURN-STOO-109", "LoftBar Leather Swivel Bar Stools (Pair)", "LoftBar", "Furniture", 179.00, ["Padded Saddle Faux Leather", "Gas Lift Height"], "360-degree swivel kitchen island counter stool"),

    # TRAVEL ACCESSORIES (4 items to bring total to exactly 113)
    ("TRAV-SUIT-110", "NomadVoyage Hardside Spinner Carry-On 21\"", "NomadVoyage", "Travel Accessories", 149.00, ["German Polycarbonate", "Hinomoto Wheels", "USB Port"], "Lightweight carry-on with Japanese silent wheels"),
    ("TRAV-PACK-111", "OrganiTravel Compression Packing Cubes 6-Set", "OrganiTravel", "Travel Accessories", 34.99, ["Double Zip Compression", "Water Resistant Nylon"], "Saves 60% luggage space neatly"),
    ("TRAV-PILL-112", "DreamFlight Ergonomic Memory Foam Pillow", "DreamFlight", "Travel Accessories", 27.50, ["360 Chin Support", "Compressible Memory Foam"], "Prevents neck stiffness on long-haul flights"),
    ("TRAV-ADAP-113", "GlobalConnect Universal Travel Adapter 35W PD", "GlobalConnect", "Travel Accessories", 24.99, ["150+ Country Compatibility", "35W USB-C PD"], "Powers 6 devices worldwide with smart fuse")
]

products.extend(extra_categories)

# Convert simple tuples into full dicts if needed
expanded_products = []
for p in products:
    if isinstance(p, dict):
        expanded_products.append(p)
    else:
        # Tuple format: sku, name, brand, category, price, features, usp
        sku, name, brand, cat, price, feats, usp = p
        expanded_products.append({
            "sku": sku,
            "name": name,
            "brand": brand,
            "category": cat,
            "price": price,
            "currency": "USD",
            "features": feats,
            "specifications": {"Warranty": "1 Year", "Quality": "Premium"},
            "target_audience": f"Shoppers interested in {cat.lower()}",
            "primary_keywords": [name.lower(), cat.lower()],
            "secondary_keywords": [brand.lower(), "retail product"],
            "usp": usp,
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80",
            "material": "High grade material",
            "dimensions": "Standard dimensions",
            "color": "Default",
            "weight": "Standard weight"
        })

print(f"Total compiled products count: {len(expanded_products)}")

# 1. Write backend/data/sample_products.json
json_path = os.path.join("data", "sample_products.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(expanded_products, f, indent=2)
print(f"Saved {len(expanded_products)} products to {json_path}")

# 2. Write backend/data/sample_products.csv
csv_path = os.path.join("data", "sample_products.csv")
headers = [
    "sku", "name", "brand", "category", "price", "currency",
    "features", "specifications", "target_audience",
    "primary_keywords", "secondary_keywords", "usp",
    "material", "dimensions", "color", "weight", "image_url"
]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for p in expanded_products:
        writer.writerow([
            p.get("sku", ""),
            p.get("name", ""),
            p.get("brand", ""),
            p.get("category", ""),
            p.get("price", ""),
            p.get("currency", "USD"),
            ", ".join(p.get("features", [])) if isinstance(p.get("features"), list) else p.get("features", ""),
            json.dumps(p.get("specifications", {})),
            p.get("target_audience", ""),
            ", ".join(p.get("primary_keywords", [])) if isinstance(p.get("primary_keywords"), list) else p.get("primary_keywords", ""),
            ", ".join(p.get("secondary_keywords", [])) if isinstance(p.get("secondary_keywords"), list) else p.get("secondary_keywords", ""),
            p.get("usp", ""),
            p.get("material", ""),
            p.get("dimensions", ""),
            p.get("color", ""),
            p.get("weight", ""),
            p.get("image_url", "")
        ])
print(f"Saved {len(expanded_products)} products to {csv_path}")

# 3. Save raw products string into seed_data.py
seed_py_path = os.path.join("app", "seed", "seed_data.py")
with open(seed_py_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace existing_count threshold from 50 to 200
code = code.replace("if existing_count >= 50:", "if existing_count >= 200:")

# Generate raw products Python string
py_raw_str = "RAW_PRODUCTS = " + json.dumps(expanded_products, indent=4)

# Replace RAW_PRODUCTS block
start_idx = code.find("RAW_PRODUCTS = [")
end_idx = code.find("\ndef seed_database(db: Session):")

if start_idx != -1 and end_idx != -1:
    new_code = code[:start_idx] + py_raw_str + code[end_idx:]
    with open(seed_py_path, "w", encoding="utf-8") as f:
        f.write(new_code)
    print(f"Updated {seed_py_path} with {len(expanded_products)} products!")
else:
    print("Could not locate RAW_PRODUCTS block in seed_data.py")
