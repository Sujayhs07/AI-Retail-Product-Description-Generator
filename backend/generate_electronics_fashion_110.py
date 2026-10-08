import json
import csv
import os

electronics = [
    # 1 - 25
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

    # 26 - 55 Electronics
    { "sku": "ELEC-TV-026", "name": "VisionPro 65-Inch 4K OLED Smart TV", "brand": "VisionPro", "category": "Electronics", "price": 1499.00, "currency": "USD", "features": ["Self-Lit OLED Pixels", "120Hz Gaming Refresh Rate", "Dolby Vision & Atmos", "HDMI 2.1 4K 120Hz"], "specifications": {"Display": "65-inch 4K OLED", "OS": "Smart OS 24"}, "target_audience": "Home cinema fans and gamers", "primary_keywords": ["65 inch oled tv", "4k 120hz gaming tv"], "secondary_keywords": ["dolby vision smart tv", "thin bezel oled television"], "usp": "Infinite contrast with self-lighting OLED pixels", "image_url": "https://images.unsplash.com/photo-1593784991095-a205069470b6?auto=format&fit=crop&w=600&q=80", "material": "Ultra-Thin Metal", "dimensions": "57.0 x 32.5 x 1.8 in", "color": "Metallic Titanium", "weight": "22.5kg" },
    { "sku": "ELEC-EAR-027", "name": "AuraSound Pro ANC Wireless Earbuds", "brand": "AuraSound", "category": "Electronics", "price": 129.99, "currency": "USD", "features": ["Adaptive Active Noise Cancellation", "32-Hour Total Battery", "Custom EQ App", "Transparency Mode"], "specifications": {"Bluetooth": "5.3", "Water Resistance": "IPX4"}, "target_audience": "Commuters and remote workers", "primary_keywords": ["anc wireless earbuds", "active noise cancelling buds"], "secondary_keywords": ["bluetooth earphones with app", "transparency mode earbuds"], "usp": "Adaptive hybrid noise control in a tiny stem design", "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=600&q=80", "material": "Polycarbonate", "dimensions": "2.1 x 1.9 x 0.9 in", "color": "Matte Black", "weight": "48g" },
    { "sku": "ELEC-MOU-028", "name": "VelocityPro Wireless Ergonomic Gaming Mouse", "brand": "VelocityPro", "category": "Electronics", "price": 79.99, "currency": "USD", "features": ["26,000 DPI Optical Sensor", "Sub-1ms Wireless Connection", "Lightweight 58g Design", "100-Hour Rechargeable Battery"], "specifications": {"Sensor": "26K DPI", "Weight": "58g"}, "target_audience": "Esports competitive gamers", "primary_keywords": ["lightweight gaming mouse", "wireless 26k dpi mouse"], "secondary_keywords": ["esports ultra light mouse", "rechargeable wireless mouse"], "usp": "Ultra-light 58g body engineered for lightning flick shots", "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=600&q=80", "material": "PTFE Feet & ABS", "dimensions": "4.9 x 2.5 x 1.5 in", "color": "White & Black", "weight": "58g" },
    { "sku": "ELEC-DOCK-029", "name": "VoltMax 12-in-1 Dual 4K USB-C Dock", "brand": "VoltMax", "category": "Electronics", "price": 149.00, "currency": "USD", "features": ["Dual 4K 60Hz HDMI Outputs", "100W Power Delivery Pass-Through", "1Gbps Ethernet & SD Card Reader", "4x USB 3.2 Ports"], "specifications": {"Power Pass-Through": "100W", "Display Output": "Dual 4K60"}, "target_audience": "Workstation users and laptop power users", "primary_keywords": ["usb c docking station", "dual 4k hdmi laptop dock"],
        "secondary_keywords": ["100w pd usb hub", "12 in 1 thunderbolt dock"], "usp": "Turns a single USB-C cable into a dual 4K workstation powerhouse", "image_url": "https://images.unsplash.com/photo-1609592424074-8848b813f8aa?auto=format&fit=crop&w=600&q=80", "material": "Aluminum Alloy", "dimensions": "5.5 x 2.5 x 0.7 in", "color": "Space Grey", "weight": "210g" },
    { "sku": "ELEC-BELL-030", "name": "SmartNest 2K Wireless Video Doorbell", "brand": "SmartNest", "category": "Electronics", "price": 119.50, "currency": "USD", "features": ["2K HD Head-to-Toe Video", "AI Package & Motion Detection", "2-Way Audio Talk", "No Monthly Fee Local Storage"], "specifications": {"Resolution": "2K 2048x1536", "Power": "Rechargeable Battery or Hardwired"}, "target_audience": "Homeowners and apartment security", "primary_keywords": ["2k video doorbell camera", "wireless smart doorbell"], "secondary_keywords": ["no subscription door camera", "ai motion doorbell"], "usp": "Head-to-toe 2K video view with built-in AI package detection", "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=600&q=80", "material": "Weatherproof ABS", "dimensions": "5.1 x 1.8 x 1.1 in", "color": "Black & Satin Nickel", "weight": "230g" },
    { "sku": "ELEC-SPLI-031", "name": "ErgoFlex Split Mechanical Wireless Keyboard", "brand": "ErgoFlex", "category": "Electronics", "price": 189.00, "currency": "USD", "features": ["Ergonomic 2-Piece Split Design", "Hot-Swappable Silent Switches", "PBT Keycaps & Bluetooth 5.2", "Built-In Palm Rests"], "specifications": {"Layout": "Split 65%", "Battery": "3000mAh"}, "target_audience": "Programmers, writers, and ergo enthusiasts", "primary_keywords": ["split mechanical keyboard", "ergonomic wireless split keyboard"], "secondary_keywords": ["wrist comfort keyboard", "hot swap split keyboard"], "usp": "Reduces shoulder strain with completely separated wireless typing halves", "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80", "material": "PBT & Aluminum", "dimensions": "7.2 x 5.8 x 1.2 in each", "color": "Charcoal Grey", "weight": "880g" },
    { "sku": "ELEC-UST-032", "name": "CineBeam 4K Ultra Short Throw Laser Projector", "brand": "CineBeam", "category": "Electronics", "price": 1899.00, "currency": "USD", "features": ["120-Inch Screen at 9 Inches Distance", "Real 4K UHD Resolution", "2500 ANSI Lumens Brightness", "Harmon Kardon Built-in Soundbar"], "specifications": {"Resolution": "4K 3840x2160", "Throw Ratio": "0.23:1"}, "target_audience": "Luxury home theater buyers", "primary_keywords": ["4k ultra short throw projector", "laser cinema projector"], "secondary_keywords": ["120 inch laser tv", "short throw 4k projector"], "usp": "Projects a massive 120-inch 4K cinema image from just inches off the wall", "image_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=600&q=80", "material": "Brushed Metal & Fabric", "dimensions": "20.8 x 14.5 x 5.2 in", "color": "Silver White", "weight": "9.8kg" },
    { "sku": "ELEC-SOLA-033", "name": "VoltMax 1000W Portable Solar Power Station", "brand": "VoltMax", "category": "Electronics", "price": 749.00, "currency": "USD", "features": ["1024Wh LiFePO4 Battery Capacity", "1000W AC Pure Sine Wave Outlets", "0-80% Recharge in 50 Minutes", "Supports 400W Solar Input"], "specifications": {"Capacity": "1024Wh", "Lifecycle": "3500+ Cycles"}, "target_audience": "RV campers, emergency prep, and outdoor events", "primary_keywords": ["portable solar generator", "1000w lifepo4 power station"], "secondary_keywords": ["solar backup battery bank", "fast charge solar station"], "usp": "Long-lasting 3500-cycle LiFePO4 battery that recharges to 80% in 50 minutes", "image_url": "https://images.unsplash.com/photo-1609592424074-8848b813f8aa?auto=format&fit=crop&w=600&q=80", "material": "Reinforced Fireproof Polymer", "dimensions": "15.7 x 8.3 x 11.0 in", "color": "Dark Grey & Yellow", "weight": "11.8kg" },
    { "sku": "ELEC-OUT-034", "name": "SmartNest Outdoor 360 Security Camera", "brand": "SmartNest", "category": "Electronics", "price": 99.99, "currency": "USD", "features": ["360° Pan & 90° Tilt Motion Tracking", "Color Night Vision with Spotlight", "IP66 Weather Resistance", "Solar Panel Powered Option"], "specifications": {"Resolution": "2K 4MP", "Rating": "IP66 Outdoor"}, "target_audience": "Home security conscious families", "primary_keywords": ["360 outdoor security camera", "pan tilt solar camera"], "secondary_keywords": ["color night vision outdoor cam", "wireless wifi security camera"], "usp": "Complete 360-degree perimeter protection with spotlight color night vision", "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=600&q=80", "material": "IP66 Weatherproof Polycarbonate", "dimensions": "6.2 x 4.1 x 3.8 in", "color": "Clean White", "weight": "410g" },
    { "sku": "ELEC-IEM-035", "name": "ClearTone Studio Dual-Driver In-Ear Monitors", "brand": "ClearTone", "category": "Electronics", "price": 149.00, "currency": "USD", "features": ["Dual Balanced Armature + Dynamic Hybrid Drivers", "Detachable MMCX Audiophile Cable", "Noise Isolation Up to 37dB", "Included Memory Foam Ear Tips"], "specifications": {"Driver": "1 BA + 1 Dynamic", "Connector": "Gold MMCX"}, "target_audience": "Musicians, stage performers, and audiophiles", "primary_keywords": ["dual driver in ear monitors", "stage iem earphones"], "secondary_keywords": ["mmcx detachable cable earbuds", "noise isolating studio iem"], "usp": "Dual hybrid driver precision for crystal clear vocals and tight stage bass", "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=600&q=80", "material": "Resin Shell & Braided Wire", "dimensions": "Universal Ergonomic Fit", "color": "Transparent Crystal", "weight": "24g" },
    { "sku": "ELEC-DAC-036", "name": "AudioPure High-Res Portable USB DAC & Amp", "brand": "AudioPure", "category": "Electronics", "price": 119.99, "currency": "USD", "features": ["ES9038Q2M Sabre DAC Chip", "Supports 32-Bit / 768kHz & DSD512", "3.5mm Single & 4.4mm Balanced Outputs", "Ultra-Low Noise Floor"], "specifications": {"DAC": "ESS Sabre 9038", "Outputs": "3.5mm & 4.4mm Bal"}, "target_audience": "Audiophiles listening via smartphones and laptops", "primary_keywords": ["portable usb dac amp", "high res headphone amplifier"], "secondary_keywords": ["ess sabre dac dongle", "4.4mm balanced dac"], "usp": "Transforms smartphone audio into studio-master 32-bit resolution", "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80", "material": "CNC Anodized Aluminum", "dimensions": "2.2 x 0.9 x 0.5 in", "color": "Gunmetal Gray", "weight": "32g" },
    { "sku": "ELEC-PUR-037", "name": "EcoClimate HEPA H13 Smart Air Purifier", "brand": "EcoClimate", "category": "Electronics", "price": 159.00, "currency": "USD", "features": ["3-Stage True HEPA H13 Filtration", "CADR 260 m³/h for Rooms Up to 500 Sq Ft", "Real-Time PM2.5 Air Quality Sensor", "Whisper Quiet 22dB Sleep Mode"], "specifications": {"Coverage": "500 sq ft", "Filter": "True HEPA H13"}, "target_audience": "Allergy sufferers, pet owners, and urban apartments", "primary_keywords": ["hepa h13 smart air purifier", "room air cleaner for allergies"], "secondary_keywords": ["pm2.5 sensor quiet purifier", "large room pet air purifier"], "usp": "Captures 99.97% of dust, pollen, and pet dander with real-time PM2.5 displays", "image_url": "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?auto=format&fit=crop&w=600&q=80", "material": "ABS Plastic", "dimensions": "14.5 x 8.5 x 8.5 in", "color": "Satin White", "weight": "3.2kg" },
    { "sku": "ELEC-PAD-038", "name": "TactilePro RGB Wireless Charging Desk Mat", "brand": "TactilePro", "category": "Electronics", "price": 49.99, "currency": "USD", "features": ["15W Fast Qi Wireless Charging Zone", "10 RGB Backlight Lighting Modes", "Ultra-Smooth Micro-Weave Cloth Surface", "Water-Resistant Coating"], "specifications": {"Size": "31.5 x 11.8 inches", "Wireless Power": "15W Max"}, "target_audience": "Gamers and clean desk setup builders", "primary_keywords": ["wireless charging desk mat", "rgb oversized mouse pad"], "secondary_keywords": ["15w fast charge mousepad", "water resistant gaming mat"], "usp": "Full desk surface pad with integrated 15W smartphone fast charging zone", "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80", "material": "Micro-Weave Cloth & Rubber Base", "dimensions": "31.5 x 11.8 x 0.15 in", "color": "Stealth Black", "weight": "620g" },
    { "sku": "ELEC-CAP-039", "name": "ApexShot 4K60 HDR USB 3.2 Capture Card", "brand": "ApexShot", "category": "Electronics", "price": 139.00, "currency": "USD", "features": ["Pass-Through 4K 60fps HDR & 1080p 240fps", "Zero-Latency Pass-Through HDMI", "Plug & Play with OBS & Twitch", "Aluminum Heatsink Casing"], "specifications": {"Capture": "1080p60 / 4K30", "Pass-Through": "4K60 HDR"}, "target_audience": "Console gamers, live streamers, and videographers", "primary_keywords": ["4k60 hdmi capture card", "game streaming capture card"], "secondary_keywords": ["obs twitch capture card", "zero latency capture dongle"], "usp": "Zero-lag 4K HDR passthrough for effortless Twitch and YouTube streaming", "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80", "material": "Aluminum Alloy", "dimensions": "4.1 x 2.4 x 0.6 in", "color": "Matte Black", "weight": "95g" },
    { "sku": "ELEC-PMON-040", "name": "VisionPro 15.6-Inch Portable Touch Monitor", "brand": "VisionPro", "category": "Electronics", "price": 199.99, "currency": "USD", "features": ["10-Point Capacitive Touchscreen", "FHD 1080P IPS Display", "Single USB-C Cable Signal & Power", "Built-in Kickstand & Dual Speakers"], "specifications": {"Screen": "15.6 in IPS 1080P", "Weight": "750g"}, "target_audience": "Laptop dual-screen workers and travelers", "primary_keywords": ["portable touchscreen monitor", "15.6 inch usb c second screen"], "secondary_keywords": ["fhd ips portable display", "kickstand travel monitor"], "usp": "Ultra-slim 10-point touchscreen second monitor powered via a single USB-C cable", "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80", "material": "CNC Aluminum", "dimensions": "14.1 x 8.8 x 0.35 in", "color": "Dark Slate", "weight": "750g" },
    { "sku": "ELEC-STRIP-041", "name": "VibePulse RGBIC 10m Smart LED Light Strip", "brand": "VibePulse", "category": "Electronics", "price": 39.99, "currency": "USD", "features": ["Segmented RGBIC Multi-Color Lighting", "Music Sync Built-in Mic", "App & Voice Control (Alexa/Google)", "Waterproof Protective Silicone Coating"], "specifications": {"Length": "32.8ft / 10m", "LEDs": "300 LEDs"}, "target_audience": "Room decorators, gamers, and party hosts", "primary_keywords": ["rgbic smart led light strip", "music sync led room lights"], "secondary_keywords": ["alexa voice control light strip", "10m waterproof led tape"], "usp": "Displays multiple rainbow colors simultaneously along one light strip", "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=600&q=80", "material": "Silicone Flexible PCB", "dimensions": "10m length", "color": "Multicolor RGBIC", "weight": "340g" },
    { "sku": "ELEC-REM-042", "name": "NovaBook Air Remote Presenter with Gyro Mouse", "brand": "NovaBook", "category": "Electronics", "price": 34.50, "currency": "USD", "features": ["2.4GHz & Bluetooth 5.0 Dual Connection", "Air Mouse Gyroscope Cursor Control", "Bright Green Laser Pointer", "Rechargeable USB-C Battery"], "specifications": {"Range": "100 feet", "Laser": "Class 2 Green"}, "target_audience": "Teachers, public speakers, and corporate executives", "primary_keywords": ["wireless presenter air mouse", "green laser pointer remote"], "secondary_keywords": ["bluetooth presentation remote", "rechargeable slide clicker"], "usp": "Intuitive air-mouse wrist motion control paired with a high-visibility green laser", "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80", "material": "Soft-Touch Polycarbonate", "dimensions": "5.3 x 1.2 x 0.8 in", "color": "Matte Black", "weight": "55g" },
    { "sku": "ELEC-PLUG-043", "name": "SmartNest WiFi Smart Plug Mini (4-Pack)", "brand": "SmartNest", "category": "Electronics", "price": 29.99, "currency": "USD", "features": ["Energy Consumption Monitoring", "Schedule & Timer Routines", "Compact Space-Saving Plug Design", "Voice Control via Alexa & Google Assistant"], "specifications": {"Max Load": "15A 1800W", "Quantity": "4 Plugs"}, "target_audience": "Smart home automation enthusiasts", "primary_keywords": ["wifi smart plug mini", "energy monitoring smart outlet"], "secondary_keywords": ["alexa smart plug 4 pack", "timer outlet for lamps"], "usp": "Monitors real-time electricity wattage while fitting 2 plugs on 1 wall outlet", "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=600&q=80", "material": "Fire-Resistant Polycarbonate", "dimensions": "2.2 x 1.5 x 1.2 in each", "color": "Pure White", "weight": "60g each" },
    { "sku": "ELEC-DESK-044", "name": "ModuDesk Touch Memory Desk Control Module", "brand": "ModuDesk", "category": "Electronics", "price": 49.00, "currency": "USD", "features": ["OLED Height Display in Inches/CM", "4 Saved Preset Height Buttons", "USB-C Charging Port Built-In", "Anti-Collision Sensitivity Setting"], "specifications": {"Voltage": "24V DC", "Ports": "USB-C 18W"}, "target_audience": "DIY standing desk upgrade builders", "primary_keywords": ["standing desk controller keypad", "oled desk height memory switch"], "secondary_keywords": ["motorized desk keypad c port", "anti collision desk controller"], "usp": "Crisp OLED height feedback with 4 memory positions and integrated fast phone charger", "image_url": "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?auto=format&fit=crop&w=600&q=80", "material": "ABS & Acrylic Touch", "dimensions": "4.2 x 1.8 x 0.9 in", "color": "Piano Black", "weight": "110g" },
    { "sku": "ELEC-THERM-045", "name": "ApexShot Handheld Thermal Imager Camera", "brand": "ApexShot", "category": "Electronics", "price": 249.00, "currency": "USD", "features": ["256x192 Thermal IR Resolution", "-4°F to 1022°F Temperature Measurement", "2.8-Inch LCD Color Display", "PC Analysis Software Included"], "specifications": {"IR Resolution": "256x192", "Accuracy": "±2°C"}, "target_audience": "Electricians, HVAC technicians, and home inspectors", "primary_keywords": ["handheld thermal imager camera", "infrared thermal imaging camera"], "secondary_keywords": ["hvac thermal camera", "electrical inspection thermal scanner"], "usp": "Detects insulation heat leaks and electrical hotspots instantly with 256x192 clarity", "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80", "material": "Drop-Proof Rubberized Polycarbonate", "dimensions": "9.1 x 3.2 x 2.8 in", "color": "Yellow & Black", "weight": "340g" },
    { "sku": "ELEC-REC-046", "name": "VocalCraft 64GB Digital Audio Voice Recorder", "brand": "VocalCraft", "category": "Electronics", "price": 49.99, "currency": "USD", "features": ["64GB Built-In Memory Holds 750 Hours", "Voice-Activated Auto Recording", "Triple Noise Reduction Microphones", "Password Protection & USB Drag Transfer"], "specifications": {"Format": "MP3 / WAV 1536kbps", "Battery": "30 Hours Continuous"}, "target_audience": "Journalists, university students, and legal professionals", "primary_keywords": ["64gb digital voice recorder", "voice activated audio recorder"], "secondary_keywords": ["noise reduction dictaphone", "lecture recorder for students"], "usp": "Captures 1536kbps studio WAV recordings with automatic voice activation", "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=600&q=80", "material": "Zinc Alloy Metal Casing", "dimensions": "3.8 x 1.0 x 0.4 in", "color": "Dark Alloy", "weight": "75g" },
    { "sku": "ELEC-TAG-047", "name": "PulseTrack Smart Bluetooth Key Tracker (4-Pack)", "brand": "PulseTrack", "category": "Electronics", "price": 39.99, "currency": "USD", "features": ["Ultra-Loud 100dB Beeper Ring", "200ft Bluetooth Range + Global Crowd Finding", "IP67 Waterproof & 1-Year Replaceable Battery", "Reverse Phone Finder Button"], "specifications": {"Battery": "CR2032 Replaceable", "Water Rating": "IP67"}, "target_audience": "People who frequently lose keys, wallets, or luggage", "primary_keywords": ["bluetooth key tracker 4 pack", "item finder tag for keys"], "secondary_keywords": ["waterproof wallet tracker tag", "loud key locator ring"], "usp": "Ultra-loud 100dB ring buzzer and crowd network location tracking for keys and bags", "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80", "material": "Polycarbonate Shell", "dimensions": "1.4 x 1.4 x 0.25 in each", "color": "Black / White / Navy / Olive", "weight": "12g each" },
    { "sku": "ELEC-SPOT-048", "name": "NetSpeed 5G WiFi 6 Mobile Hotspot Router", "brand": "NetSpeed", "category": "Electronics", "price": 249.00, "currency": "USD", "features": ["5G Sub-6GHz Speeds Up to 2.5Gbps", "WiFi 6 Connects Up to 32 Devices", "5000mAh Battery for 12 Hours Use", "Color Touchscreen Data Display"], "specifications": {"Networks": "Unlocked 5G LTE", "WiFi": "WiFi 6 Dual Band"}, "target_audience": "Digital nomads, remote workers, and international travelers", "primary_keywords": ["5g mobile hotspot router", "unlocked wifi 6 travel hotspot"], "secondary_keywords": ["portable 5g internet dongle", "high speed mobile router"], "usp": "Blazing 2.5Gbps 5G WiFi 6 coverage for 32 devices anywhere you travel", "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=600&q=80", "material": "Satin Touch Polycarbonate", "dimensions": "4.9 x 2.8 x 0.6 in", "color": "Midnight Black", "weight": "185g" },
    { "sku": "ELEC-LAV-049", "name": "VocalCraft Wireless Dual Lavalier Microphone Kit", "brand": "VocalCraft", "category": "Electronics", "price": 79.99, "currency": "USD", "features": ["2 Transmitters + 1 Receiver for Dual Person Interviews", "Active AI Noise Cancellation Chip", "65ft Stable Wireless Range", "Plug & Play for iPhone / Android / Camera"], "specifications": {"Latency": "0.009s Ultra-low", "Battery": "7 hours per mic"}, "target_audience": "Vloggers, interviewers, TikTok creators, and journalists", "primary_keywords": ["wireless dual lavalier microphone", "clip on mic for phone video"], "secondary_keywords": ["wireless lapel mic dual pack", "noise cancelling vlog microphone"], "usp": "Instant 2-person interview mic setup with AI noise filtering and 0.009s latency", "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=600&q=80", "material": "ABS Plastic", "dimensions": "1.8 x 0.8 x 0.5 in each", "color": "Matte Black", "weight": "18g each" },
    { "sku": "ELEC-LEAK-050", "name": "SmartNest WiFi Smart Water Leak Sensor Alarm", "brand": "SmartNest", "category": "Electronics", "price": 24.99, "currency": "USD", "features": ["Dual Top & Bottom Probe Leak Sensing", "Instant Phone App Push Notification + 100dB Siren", "IP67 Waterproof Floating Body", "2-Year Battery Life"], "specifications": {"Buzzer": "100dB Local Alarm", "Battery": "2x AAA"}, "target_audience": "Homeowners protecting basements, sinks, and water heaters", "primary_keywords": ["wifi water leak sensor alarm", "smart flood detector for home"], "secondary_keywords": ["basement water alarm app alert", "waterproof leak detector"], "usp": "Instant 100dB siren and smartphone push alert at the first micro drop of water", "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=600&q=80", "material": "IP67 Sealed Polycarbonate", "dimensions": "2.8 x 2.8 x 1.0 in", "color": "Clean White", "weight": "85g" },
    { "sku": "ELEC-OLED49-051", "name": "VisionPro 49-Inch Super Ultrawide OLED Monitor", "brand": "VisionPro", "category": "Electronics", "price": 1199.00, "currency": "USD", "features": ["32:9 Dual QHD 5120x1440 OLED", "240Hz Refresh Rate & 0.03ms Response Time", "1800R Immersive Curvature", "Built-in KVM Switch for 2 PCs"], "specifications": {"Resolution": "5120 x 1440 OLED", "Refresh Rate": "240Hz"}, "target_audience": "Sim racers, day traders, and extreme gamers", "primary_keywords": ["49 inch super ultrawide oled", "240hz 32:9 gaming monitor"], "secondary_keywords": ["dual qhd curved oled screen", "kvm switch gaming monitor"], "usp": "Replaces two 27-inch QHD monitors with one seamless 240Hz OLED curve", "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80", "material": "Aluminum & Steel Base", "dimensions": "47.0 x 21.0 x 11.5 in", "color": "Titanium Silver", "weight": "11.2kg" },
    { "sku": "ELEC-PET-052", "name": "SmartNest Automatic Pet Feeder with 1080P Camera", "brand": "SmartNest", "category": "Electronics", "price": 99.00, "currency": "USD", "features": ["Scheduled & Portion-Controlled Feeding", "1080P Night Vision HD Camera & 2-Way Audio", "Desiccant Bag Freshness Seal", "Dual Power Supply Backup"], "specifications": {"Capacity": "4 Liters Dry Food", "Camera": "1080P Wide Angle"}, "target_audience": "Cat and dog owners who travel or work long hours", "primary_keywords": ["automatic pet feeder with camera", "smart cat food dispenser app"], "secondary_keywords": ["portion control dog feeder", "timed pet feeder 2 way audio"], "usp": "Watch and speak to your pet live while scheduling precise automatic meals", "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=600&q=80", "material": "Food-Grade ABS & Stainless Bowl", "dimensions": "13.2 x 7.5 x 7.5 in", "color": "White & Stainless Steel", "weight": "2.1kg" },
    { "sku": "ELEC-STAN-053", "name": "VocalCraft Studio Mic Boom Arm Stand Bundle", "brand": "VocalCraft", "category": "Electronics", "price": 45.00, "currency": "USD", "features": ["Heavy Duty Internal Spring Suspension Arm", "Integrated Hidden Cable Management Channel", "360° Smooth Silent Rotation", "Includes Universal Shock Mount & Pop Filter"], "specifications": {"Reach": "32 inches", "Max Load": "4.4 lbs / 2.0kg"}, "target_audience": "Streamers, podcasters, and radio announcers", "primary_keywords": ["microphone boom arm stand bundle", "heavy duty studio mic arm"], "secondary_keywords": ["desk clamp broadcast mic arm", "shock mount pop filter set"], "usp": "Whisper-quiet internal springs hold heavy studio mics securely without sagging", "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=600&q=80", "material": "Powder-Coated Steel", "dimensions": "16 in + 16 in arm length", "color": "Matte Black", "weight": "1.3kg" },
    { "sku": "ELEC-FOLDKEY-054", "name": "TactilePro Pocket Foldable Bluetooth Keyboard", "brand": "TactilePro", "category": "Electronics", "price": 38.99, "currency": "USD", "features": ["Tri-Folding Pocket Size Design", "Integrated Touchpad Mouse", "Connects Up to 3 Devices Simultaneously", "60 Hours Typing Battery"], "specifications": {"Folded Size": "6.0 x 3.8 x 0.6 in", "Connection": "Bluetooth 5.1 x3"}, "target_audience": "Tablet typing travelers and phone productivity users", "primary_keywords": ["foldable bluetooth keyboard touchpad", "pocket wireless keyboard"], "secondary_keywords": ["tri fold travel keyboard", "multi device tablet keyboard"], "usp": "Folds down to pocket phone size while featuring a full responsive touchpad", "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80", "material": "Aluminum Outer Case", "dimensions": "11.8 x 3.8 x 0.3 in (Unfolded)", "color": "Space Gray", "weight": "210g" },
    { "sku": "ELEC-MAGBAT-055", "name": "VoltMax 10000mAh MagSafe Power Bank Stand", "brand": "VoltMax", "category": "Electronics", "price": 49.99, "currency": "USD", "features": ["Strong 12N Magnetic Snap Lock", "Built-in Foldable Metal Kickstand", "20W USB-C PD Fast Input/Output", "15W Wireless Fast Charging"], "specifications": {"Capacity": "10000mAh", "Wireless Output": "15W Max"}, "target_audience": "iPhone and MagSafe smartphone users", "primary_keywords": ["magsafe power bank 10000mah", "magnetic wireless charger stand"], "secondary_keywords": ["portable battery with kickstand", "fast charging wireless powerbank"], "usp": "Snaps firmly to phone back with integrated kickstand for video viewing while charging", "image_url": "https://images.unsplash.com/photo-1609592424074-8848b813f8aa?auto=format&fit=crop&w=600&q=80", "material": "Soft Rubber & Metal Stand", "dimensions": "4.1 x 2.6 x 0.7 in", "color": "Midnight Black", "weight": "205g" }
]

fashion = [
    # 1 - 25
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
    },

    # 26 - 55 Fashion
    { "sku": "FASH-SHIR-051", "name": "PureLinen French Linen Summer Button-Down", "brand": "PureLinen", "category": "Fashion", "price": 65.00, "currency": "USD", "features": ["100% European Organic Linen", "Relaxed Fit Resort Collar", "Pre-Washed Vintage Softness", "Mother of Pearl Shell Buttons"], "specifications": {"Material": "100% Linen", "Fit": "Resort Casual"}, "target_audience": "Beach vacationers, summer casual dressers", "primary_keywords": ["linen button down shirt", "men French linen resort shirt"], "secondary_keywords": ["breathable summer shirt", "organic linen long sleeve"], "usp": "Ultra-breathable European organic linen pre-washed for instant breezy comfort", "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=600&q=80", "material": "100% French Linen", "dimensions": "Men S-XXL", "color": "Sky Blue", "weight": "210g" },
    { "sku": "FASH-WRAP-052", "name": "CashmereLux Open Front Cardigan Wrap", "brand": "CashmereLux", "category": "Fashion", "price": 149.00, "currency": "USD", "features": ["100% Grade-A Mongolian Cashmere", "Draped Open-Front Design", "Ribbed Sleeve Cuffs & Hem", "Ultra-Lightweight 2-Ply Knit"], "specifications": {"Grade": "100% Mongolian Cashmere", "Ply": "2-Ply 12-Gauge"}, "target_audience": "Women seeking luxury flight and office layering", "primary_keywords": ["mongolian cashmere cardigan", "women open front wrap"], "secondary_keywords": ["soft cashmere shawl sweater", "luxury travel cardigan"], "usp": "Pure 100% Grade-A Mongolian cashmere with effortless open-front drape", "image_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=600&q=80", "material": "100% Cashmere", "dimensions": "One Size Draped", "color": "Camel Beige", "weight": "290g" },
    { "sku": "FASH-TRAIL-053", "name": "TerraTrek Waterproof Trail Running Shoes", "brand": "TerraTrek", "category": "Fashion", "price": 135.00, "currency": "USD", "features": ["Gore-Tex Waterproof Membrane", "Vibram Megagrip 5mm Lugs", "Quick-Lace Speed Toggle", "Rock Plate Underfoot Protection"], "specifications": {"Waterproof": "Gore-Tex", "Drop": "6mm"}, "target_audience": "Trail runners and mud hikers", "primary_keywords": ["gore tex trail running shoes", "vibram lugged sneakers"], "secondary_keywords": ["waterproof trail runners", "quick lace hiking sneakers"], "usp": "Vibram Megagrip traction with Gore-Tex waterproof protection on slippery trails", "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80", "material": "Ripstop & Gore-Tex", "dimensions": "US Mens 7-13", "color": "Forest Green & Orange", "weight": "310g" },
    { "sku": "FASH-MESS-054", "name": "CraftLeather Italian Leather Messenger Bag", "brand": "CraftLeather", "category": "Fashion", "price": 199.00, "currency": "USD", "features": ["Full-Grain Italian Cowhide Leather", "Fits Up to 15.6-Inch Laptops", "Antique Brass Hardware & Quick Clasp", "Padded Adjustable Shoulder Strap"], "specifications": {"Capacity": "14 Liters", "Fit": "15.6\" Laptop"}, "target_audience": "Commuters, lawyers, and students", "primary_keywords": ["leather messenger bag", "men italian leather briefcase"], "secondary_keywords": ["full grain satchel bag", "laptop shoulder briefcase"], "usp": "Full-grain Italian cowhide structured for rugged professional daily carry", "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=600&q=80", "material": "Full-Grain Italian Leather", "dimensions": "16.0 x 11.5 x 4.0 in", "color": "Dark Chestnut", "weight": "1.2kg" },
    { "sku": "FASH-TUX-055", "name": "SavileRow Italian Wool Slim Fit Tuxedo", "brand": "SavileRow", "category": "Fashion", "price": 399.00, "currency": "USD", "features": ["Super 130s Italian Virgin Wool", "Satin Peak Lapel & Satin Side Stripe", "Half-Canvas Tailored Structure", "Includes Satin Trimmed Trousers"], "specifications": {"Fabric": "Super 130s Wool", "Lapel": "Satin Peak"}, "target_audience": "Grooms, black-tie event attendees, and gala guests", "primary_keywords": ["italian wool tuxedo suit", "black tie peak lapel tuxedo"], "secondary_keywords": ["men slim fit tuxedo", "super 130s formal suit"], "usp": "Super 130s virgin wool half-canvas tuxedo for timeless black-tie elegance", "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=600&q=80", "material": "100% Virgin Wool & Satin", "dimensions": "Sizes 36R-48R", "color": "Jet Black", "weight": "1.4kg" },
    { "sku": "FASH-LEGG-056", "name": "CloudStride Seamless High-Waist Yoga Leggings", "brand": "CloudStride", "category": "Fashion", "price": 54.00, "currency": "USD", "features": ["Squat-Proof 4-Way Stretch Compression", "High-Waist Tummy Control Band", "Hidden Back Waistband Pocket", "Moisture-Wicking Butter-Soft Nylon"], "specifications": {"Inseam": "25 inches", "Waist": "High Rise"}, "target_audience": "Yogis, pilates practitioners, and gym goers", "primary_keywords": ["high waist yoga leggings", "squat proof athletic tights"], "secondary_keywords": ["seamless buttery soft leggings", "tummy control workout pants"], "usp": "Squat-proof compression with buttery soft zero-chafing feel", "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=600&q=80", "material": "80% Nylon, 20% Elastane", "dimensions": "Women XS-XL", "color": "Plum Dark Berry", "weight": "195g" },
    { "sku": "FASH-BIKE-057", "name": "HeritageVintage Classic Lambskin Leather Jacket", "brand": "HeritageVintage", "category": "Fashion", "price": 289.00, "currency": "USD", "features": ["100% Ultra-Soft Lambskin Leather", "Asymmetric Heavy Metal Zipper", "Quilted Shoulder Accents", "Satin Smooth Inner Lining"], "specifications": {"Leather": "100% Lambskin Nappa", "Hardware": "Silver Steel"}, "target_audience": "Motorcycle fans and edgy streetwear dressers", "primary_keywords": ["leather biker jacket", "men lambskin moto jacket"], "secondary_keywords": ["asymmetric zipper leather coat", "real leather motorcycle jacket"], "usp": "Supple 100% lambskin nappa leather featuring timeless moto zip detailing", "image_url": "https://images.unsplash.com/photo-1521223890158-f9f7c3d5d504?auto=format&fit=crop&w=600&q=80", "material": "Lambskin Leather", "dimensions": "Men S-XXL", "color": "Stealth Black", "weight": "1.3kg" },
    { "sku": "FASH-DRES-058", "name": "VogueParis Ribbed Knit Bodycon Midi Dress", "brand": "VogueParis", "category": "Fashion", "price": 78.00, "currency": "USD", "features": ["Stretch Cotton Viscose Ribbed Knit", "Flattering Mock Neckline", "Side Leg Slit for Movement", "Form-Fitting Silhouette"], "specifications": {"Length": "Midi", "Knit": "Fine Ribbed"}, "target_audience": "Women seeking stylish dinner or party dresses", "primary_keywords": ["ribbed knit midi dress", "mock neck bodycon dress"], "secondary_keywords": ["women side slit knit dress", "elegant autumn midi dress"], "usp": "Sculpting fine ribbed knit with a high mock neck and subtle side leg slit", "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=600&q=80", "material": "70% Viscose, 30% Cotton", "dimensions": "Women XS-L", "color": "Terracotta Rust", "weight": "340g" },
    { "sku": "FASH-DUFF-059", "name": "NomadVoyage Heavy Canvas Weekend Duffle Bag", "brand": "NomadVoyage", "category": "Fashion", "price": 89.00, "currency": "USD", "features": ["16 oz Heavy Duty Waxed Canvas", "Full-Grain Leather Handles & Trim", "Separate Shoe Compartment", "Detachable Padded Shoulder Strap"], "specifications": {"Capacity": "45 Liters", "Flight": "Carry-On Approved"}, "target_audience": "Weekend travelers, road trippers, and gym goers", "primary_keywords": ["waxed canvas duffle bag", "men leather trim travel bag"], "secondary_keywords": ["weekender bag with shoe compartment", "overnight gym duffel"], "usp": "Water-repellent 16oz waxed canvas with a dedicated zippered shoe pocket", "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80", "material": "Waxed Canvas & Leather", "dimensions": "21.0 x 12.0 x 11.0 in", "color": "Olive Drab & Brown Leather", "weight": "1.4kg" },
    { "sku": "FASH-PARK-060", "name": "UrbanShield Sub-Zero Waterproof Winter Parka", "brand": "UrbanShield", "category": "Fashion", "price": 259.00, "currency": "USD", "features": ["Synthetic Down Insulation Rated to -20°F", "20,000mm Waterproof Shell", "Faux-Fur Trimmed Removable Hood", "Fleece-Lined Storm Pockets"], "specifications": {"Temp Rating": "-20°F / -28°C", "Waterproof": "20,000mm"}, "target_audience": "Extreme cold winter commuters and skiers", "primary_keywords": ["sub zero winter parka", "waterproof faux fur hood coat"], "secondary_keywords": ["heavy winter parka jacket", "warm sub zero coat"], "usp": "Rated to -20°F with 20,000mm waterproof storm protection", "image_url": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=600&q=80", "material": "Polyester & Synthetic Down", "dimensions": "Sizes S-XXL", "color": "Midnight Navy", "weight": "1.6kg" },
    { "sku": "FASH-WATC-061", "name": "SolStyle Minimalist Stainless Steel Watch", "brand": "SolStyle", "category": "Fashion", "price": 95.00, "currency": "USD", "features": ["Japanese Quartz Movement", "316L Surgical Stainless Steel Mesh Strap", "Sapphire Crystal Scratch-Resistant Glass", "50m Water Resistance"], "specifications": {"Case Diameter": "40mm", "Glass": "Sapphire Crystal"}, "target_audience": "Minimalist dressers and daily watch wearers", "primary_keywords": ["minimalist stainless steel watch", "sapphire glass quartz watch"], "secondary_keywords": ["mesh strap dress watch", "ultra thin mens watch"], "usp": "Scratch-resistant sapphire crystal paired with ultra-thin 316L mesh band", "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80", "material": "316L Stainless Steel & Sapphire", "dimensions": "40mm case", "color": "Silver & White Dial", "weight": "85g" },
    { "sku": "FASH-VISO-062", "name": "PanamaCraft Wide Brim Foldable Sun Visor", "brand": "PanamaCraft", "category": "Fashion", "price": 26.00, "currency": "USD", "features": ["UPF 50+ Extra-Wide 4.5-Inch Brim", "Roll-Up Packable Ribbon Design", "Adjustable Velcro Back Closure", "Open Top for High Ponytails"], "specifications": {"Brim": "4.5 inches", "UPF": "50+"}, "target_audience": "Gardeners, golfers, beach lovers, and walkers", "primary_keywords": ["packable sun visor hat", "upf 50 wide brim visor"], "secondary_keywords": ["open top ponytail sun hat", "roll up straw visor"], "usp": "Protects face with UPF 50+ wide shade while rolling up compact into your bag", "image_url": "https://images.unsplash.com/photo-1514327605112-b887c0e61c0a?auto=format&fit=crop&w=600&q=80", "material": "Paper Straw & Elastic", "dimensions": "Brim 4.5 in", "color": "Natural Beige", "weight": "90g" },
    { "sku": "FASH-FEDO-063", "name": "AlpineKnit 100% Wool Felt Fedora Hat", "brand": "AlpineKnit", "category": "Fashion", "price": 69.00, "currency": "USD", "features": ["100% Australian Wool Felt", "Water-Repellent & Crushable Rollable Shape", "Genuine Leather Band Trim", "Interior Adjustable Drawstring"], "specifications": {"Material": "100% Australian Wool Felt", "Style": "Wide Brim Fedora"}, "target_audience": "Fall fashion dressers and music festival goers", "primary_keywords": ["wool felt fedora hat", "crushable wide brim hat"], "secondary_keywords": ["men women wool fedora", "leather band felt hat"], "usp": "Crushable Australian wool felt that springs back into perfect shape", "image_url": "https://images.unsplash.com/photo-1514327605112-b887c0e61c0a?auto=format&fit=crop&w=600&q=80", "material": "100% Wool Felt & Leather", "dimensions": "Brim 3.0 in", "color": "Dark Olive Green", "weight": "140g" },
    { "sku": "FASH-WIND-064", "name": "VelocityPro Ultralight Running Windbreaker", "brand": "VelocityPro", "category": "Fashion", "price": 59.00, "currency": "USD", "features": ["Packs Into Its Own Zippered Chest Pocket", "Windproof & DWR Water-Repellent Coating", "360° High-Vis Reflective Strips", "Underarm Laser Mesh Ventilation"], "specifications": {"Weight": "110g Featherlight", "Material": "100% Nylon"}, "target_audience": "Night runners and marathon trainers", "primary_keywords": ["packable running windbreaker", "reflective lightweight jacket"], "secondary_keywords": ["windproof running jacket", "110g ultralight windbreaker"], "usp": "Weighs only 110g and packs into its own pocket with 360° reflective safety", "image_url": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=600&q=80", "material": "20D Ripstop Nylon", "dimensions": "Unisex XS-XXL", "color": "Neon Lime", "weight": "110g" },
    { "sku": "FASH-MOCC-065", "name": "MilanoCraft Genuine Suede Driving Moccasins", "brand": "MilanoCraft", "category": "Fashion", "price": 119.00, "currency": "USD", "features": ["Hand-Stitched Italian Calf Suede", "Rubber Pebble Driver Sole & Heel Guard", "Breathable Leather Lining", "Slip-On Ergonomic Comfort"], "specifications": {"Sole": "Rubber Pebble Driver", "Upper": "Calf Suede"}, "target_audience": "Casual drivers and summer stylish dressers", "primary_keywords": ["suede driving moccasins", "men rubber pebble sole shoes"], "secondary_keywords": ["hand stitched slip on loafers", "italian suede driver shoes"], "usp": "Flexible rubber pebble driver sole crafted from buttery soft Italian suede", "image_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=600&q=80", "material": "Calf Suede & Rubber", "dimensions": "US Mens 7-13", "color": "Navy Blue Suede", "weight": "360g" },
    { "sku": "FASH-WAY-066", "name": "SolStyle Classic Polarized Wayfarer Sunglasses", "brand": "SolStyle", "category": "Fashion", "price": 39.99, "currency": "USD", "features": ["TAC HD Polarized Lenses", "Lightweight Acetate Frame", "UV400 100% UVA/UVB Filter", "Durable Metal Hinge Reinforcement"], "specifications": {"Lens Width": "52mm", "Bridge": "18mm"}, "target_audience": "Beachgoers, drivers, and daily sun wearers", "primary_keywords": ["polarized wayfarer sunglasses", "classic square sun glasses"], "secondary_keywords": ["uv400 acetate shades", "unisex black wayfarers"], "usp": "Timeless square wayfarer silhouette with high-definition TAC polarized clarity", "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=600&q=80", "material": "Acetate Frame & TAC Lenses", "dimensions": "Standard Adult", "color": "Matte Black & G15 Lens", "weight": "32g" },
    { "sku": "FASH-PAJ-067", "name": "SilkFlora 100% Mulberry Silk Pajama Set", "brand": "SilkFlora", "category": "Fashion", "price": 179.00, "currency": "USD", "features": ["100% Pure 19-Momme Mulberry Silk", "Button-Down Piping Collar Shirt", "Elastic Waistband Pants with Pockets", "Naturally Temperature Regulating"], "specifications": {"Silk Grade": "19-Momme Grade 6A", "Includes": "Top & Pants"}, "target_audience": "Luxury sleepwear lovers and gift seekers", "primary_keywords": ["100 mulberry silk pajama set", "women luxury silk sleepwear"], "secondary_keywords": ["19 momme silk pjs", "button down silk nightwear"], "usp": "19-momme pure mulberry silk offering unmatched skin hydration during sleep", "image_url": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?auto=format&fit=crop&w=600&q=80", "material": "100% Mulberry Silk", "dimensions": "Women S-XL", "color": "Champagne Pearl", "weight": "380g" },
    { "sku": "FASH-COMP-068", "name": "VelocityPro Athletic Compression Shirt", "brand": "VelocityPro", "category": "Fashion", "price": 34.00, "currency": "USD", "features": ["Targeted Muscle Group Compression", "Flatlock Anti-Chafing Seams", "UPF 50+ Sun Block Rating", "Quick-Dry Moisture Management"], "specifications": {"Sleeve": "Long Sleeve", "Compression": "Gradient Medium"}, "target_audience": "Athletes, weightlifters, and runners", "primary_keywords": ["athletic compression shirt", "men long sleeve base layer"], "secondary_keywords": ["dry fit workout compression", "upf 50 gym shirt"], "usp": "Gradient muscle compression that stabilizes shoulders and speeds recovery", "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=600&q=80", "material": "85% Polyester, 15% Spandex", "dimensions": "Men S-XXL", "color": "Stealth Charcoal", "weight": "180g" },
    { "sku": "FASH-OVERJ-069", "name": "HeritageVintage Oversized Trucker Denim Jacket", "brand": "HeritageVintage", "category": "Fashion", "price": 89.50, "currency": "USD", "features": ["100% Rigid Cotton Denim", "Drop-Shoulder Relaxed Cut", "Dual Chest Button Pockets", "Vintage Washed Distressing"], "specifications": {"Fit": "Oversized Unisex", "Weight": "12 oz Denim"}, "target_audience": "Streetwear fashion dressers and youth", "primary_keywords": ["oversized denim trucker jacket", "vintage washed jean jacket"], "secondary_keywords": ["drop shoulder denim coat", "unisex casual jean jacket"], "usp": "Relaxed drop-shoulder cut crafted from authentic 12oz vintage washed cotton", "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=600&q=80", "material": "100% Cotton Denim", "dimensions": "Unisex S-XL", "color": "Medium Acid Wash", "weight": "850g" },
    { "sku": "FASH-CROSS-070", "name": "LuxeLeather Woven Leather Crossbody Bag", "brand": "LuxeLeather", "category": "Fashion", "price": 129.00, "currency": "USD", "features": ["Hand-Woven Nappa Leather Pattern", "Adjustable Leather Strap", "Main Zippered Compartment + Card Slots", "Gold Metal Accent Hardware"], "specifications": {"Dimensions": "9.5 x 6.5 x 2.5 in", "Strap": "48 in Adjustable"}, "target_audience": "Women daily commuters and evening dressers", "primary_keywords": ["woven leather crossbody bag", "handcrafted nappa leather purse"], "secondary_keywords": ["small woven shoulder bag", "luxury leather camera bag"], "usp": "Intricately hand-woven nappa leather with adjustable crossbody strap", "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=600&q=80", "material": "Full-Grain Nappa Leather", "dimensions": "9.5 x 6.5 x 2.5 in", "color": "Butter Cream", "weight": "390g" },
    { "sku": "FASH-TERRY-071", "name": "CozyHaven Heavyweight French Terry Sweatpants", "brand": "CozyHaven", "category": "Fashion", "price": 64.00, "currency": "USD", "features": ["400 GSM Heavyweight Organic French Terry", "Deep Zippered Side Pockets", "Elastic Ankle Cuffs & Drawstring Waist", "Pre-Shrunk Premium Cotton"], "specifications": {"Weight": "400 GSM Heavy", "Leg": "Cuffed Ankle"}, "target_audience": "Loungewear lovers and streetwear dressers", "primary_keywords": ["heavyweight french terry sweatpants", "400 gsm organic cotton joggers"], "secondary_keywords": ["cozy thick sweatpants", "cuffed ankle cotton joggers"], "usp": "Heavyweight 400 GSM organic French terry that stays cozy without bagging out", "image_url": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?auto=format&fit=crop&w=600&q=80", "material": "100% Organic French Terry", "dimensions": "Unisex XS-XXL", "color": "Washed Sage Green", "weight": "650g" },
    { "sku": "FASH-SKAT-072", "name": "CloudStride Slip-On Canvas Skate Sneakers", "brand": "CloudStride", "category": "Fashion", "price": 49.99, "currency": "USD", "features": ["Heavy Duty 12oz Canvas Upper", "Vulcanized High-Traction Rubber Sole", "Padded Collar & Elastic Side Accents", "Cushioned Foam Insole"], "specifications": {"Sole": "Vulcanized Rubber", "Closure": "Slip-On"}, "target_audience": "Skaters, students, and casual shoe wearers", "primary_keywords": ["slip on canvas skate shoes", "vulcanized rubber sneakers"], "secondary_keywords": ["casual low top canvas loafers", "comfortable skate sneakers"], "usp": "Durable 12oz canvas paired with a high-grip vulcanized rubber waffle sole", "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80", "material": "12oz Cotton Canvas & Rubber", "dimensions": "US Mens 6-13", "color": "Checkered Black & White", "weight": "380g" },
    { "sku": "FASH-INFI-073", "name": "AlpineKnit Cable Knit Wool Infinity Scarf", "brand": "AlpineKnit", "category": "Fashion", "price": 35.00, "currency": "USD", "features": ["Double Loop Infinity Circle Design", "Soft Wool Blend Thermal Cable Knit", "Itch-Free Plush Texture", "Generous 55-Inch Loop Length"], "specifications": {"Loop Length": "55 inches", "Width": "12 inches"}, "target_audience": "Winter commuters and outdoor style seekers", "primary_keywords": ["cable knit infinity scarf", "double loop wool circle scarf"], "secondary_keywords": ["warm winter infinity cowl", "itch free knit neck warmer"], "usp": "Double-loop infinity circle knit providing instant wrap-around winter warmth", "image_url": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?auto=format&fit=crop&w=600&q=80", "material": "50% Wool, 50% Acrylic", "dimensions": "55 x 12 in loop", "color": "Oatmeal Cream", "weight": "240g" },
    { "sku": "FASH-COAT-074", "name": "SavileRow Wool Blend Tailored Overcoat", "brand": "SavileRow", "category": "Fashion", "price": 249.00, "currency": "USD", "features": ["70% Melton Wool Blend Insulation", "Classic Notch Lapel Single-Breasted Cut", "Interior Welt Pockets & Back Center Vent", "Fully Lined Satin Interior"], "specifications": {"Material": "70% Wool, 30% Polyamide", "Length": "Above Knee"}, "target_audience": "Executives, commuters, and winter dressers", "primary_keywords": ["men wool melton overcoat", "single breasted winter coat"], "secondary_keywords": ["tailored dress wool jacket", "notch lapel camel coat"], "usp": "70% Melton wool blend tailored in a sharp single-breasted notch lapel cut", "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=600&q=80", "material": "70% Wool Melton", "dimensions": "Sizes 38R-46R", "color": "Classic Camel Tan", "weight": "1.4kg" },
    { "sku": "FASH-POLO-075", "name": "VelocityPro Quick-Dry Performance Golf Polo", "brand": "VelocityPro", "category": "Fashion", "price": 48.00, "currency": "USD", "features": ["4-Way Stretch Micro-Pique Fabric", "UPF 40+ Sun Protection", "Self-Fabric Anti-Curl Collar", "Moisture-Wicking & Anti-Odor Technology"], "specifications": {"Fit": "Athletic Regular", "Placket": "3-Button"}, "target_audience": "Golfers, tennis players, and business casual workers", "primary_keywords": ["performance golf polo shirt", "quick dry upf 40 polo"], "secondary_keywords": ["men stretch athletic polo", "anti curl collar shirt"], "usp": "Micro-pique breathability with anti-curl collar engineered for the golf course", "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=600&q=80", "material": "92% Polyester, 8% Spandex", "dimensions": "Men S-XXL", "color": "Navy Blue Stripe", "weight": "190g" }
]

all_products = electronics + fashion
print(f"Total compiled strictly Electronics ({len(electronics)}) + Fashion ({len(fashion)}) = {len(all_products)} products")

# Write to data/sample_products.json
json_path = os.path.join("data", "sample_products.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=2)
print(f"Saved {len(all_products)} products to {json_path}")

# Write to data/sample_products.csv
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
    for p in all_products:
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
print(f"Saved {len(all_products)} products to {csv_path}")

# Update seed_data.py
seed_py_path = os.path.join("app", "seed", "seed_data.py")
with open(seed_py_path, "r", encoding="utf-8") as f:
    code = f.read()

py_raw_str = "RAW_PRODUCTS = " + json.dumps(all_products, indent=4)

start_idx = code.find("RAW_PRODUCTS = [")
end_idx = code.find("\ndef seed_database(db: Session):")

if start_idx != -1 and end_idx != -1:
    new_code = code[:start_idx] + py_raw_str + code[end_idx:]
    with open(seed_py_path, "w", encoding="utf-8") as f:
        f.write(new_code)
    print(f"Updated {seed_py_path} with {len(all_products)} Electronics & Fashion products!")
else:
    print("Could not locate RAW_PRODUCTS block in seed_data.py")
