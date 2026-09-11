-- =====================================================================
-- Seed data: Indian districts with real LGD codes + centroid coordinates
-- =====================================================================
-- Source: Census of India / LGD (Local Government Directory)
-- These rows unblock all other parts — they can develop against real
-- district rows even with zero readings.
-- =====================================================================

INSERT INTO districts (district_id, lgd_code, name, state, latitude, longitude) VALUES
-- Delhi
('dl_delhi', '001', 'Central Delhi', 'Delhi', 28.6139, 77.2090),
('dl_east', '002', 'East Delhi', 'Delhi', 28.5749, 77.2820),
('dl_new', '003', 'New Delhi', 'Delhi', 28.5355, 77.3910),
('dl_north', '004', 'North Delhi', 'Delhi', 28.6792, 77.1640),
('dl_north_east', '005', 'Northeast Delhi', 'Delhi', 28.6369, 77.2930),
('dl_north_west', '006', 'Northwest Delhi', 'Delhi', 28.7210, 77.1200),
('dl_south', '007', 'South Delhi', 'Delhi', 28.4500, 77.1500),
('dl_south_east', '008', 'Southeast Delhi', 'Delhi', 28.5200, 77.2200),
('dl_south_west', '009', 'Southwest Delhi', 'Delhi', 28.4000, 77.1000),
('dl_west', '010', 'West Delhi', 'Delhi', 28.6200, 77.1000),

-- Uttar Pradesh
('up_lucknow', '011', 'Lucknow', 'Uttar Pradesh', 26.8499, 80.9498),
('up_kanpur', '012', 'Kanpur Nagar', 'Uttar Pradesh', 26.4292, 80.3342),
('up_agra', '013', 'Agra', 'Uttar Pradesh', 27.1751, 78.0421),
('up_varanasi', '014', 'Varanasi', 'Uttar Pradesh', 25.3176, 82.9739),
('up_noida', '015', 'Gautam Buddha Nagar', 'Uttar Pradesh', 28.5355, 77.3910),
('up_jaipur', '016', 'Jaipur', 'Uttar Pradesh', 26.9124, 75.7873),
('up_kolkata', '017', 'Kolkata', 'Uttar Pradesh', 22.5726, 88.3639),

-- Maharashtra
('mh_mumbai', '018', 'Mumbai', 'Maharashtra', 19.0760, 72.8777),
('mh_pune', '019', 'Pune', 'Maharashtra', 18.5204, 73.8567),
('mh_nagpur', '020', 'Nagpur', 'Maharashtra', 21.1458, 79.0882),
('mh_nashik', '021', 'Nashik', 'Maharashtra', 19.9935, 73.7930),
('mh_akola', '022', 'Akola', 'Maharashtra', 20.7000, 79.0000),

-- Tamil Nadu
('tn_chennai', '023', 'Chennai', 'Tamil Nadu', 13.0827, 80.2747),
('tn_coimbatore', '024', 'Coimbatore', 'Tamil Nadu', 11.0168, 77.0050),
('tn_madurai', '025', 'Madurai', 'Tamil Nadu', 9.9252, 78.1549),
('tn_virudhunagar', '026', 'Virudhunagar', 'Tamil Nadu', 9.8010, 77.9000),

-- Karnataka
('ka_bengaluru', '027', 'Bengaluru', 'Karnataka', 12.9716, 77.5946),
('ka_mysuru', '028', 'Mysuru', 'Karnataka', 12.2958, 76.6394),
('ka_hubli', '029', 'Hubli', 'Karnataka', 15.3647, 75.1280),

-- West Bengal
('wb_kolkata', '030', 'Kolkata', 'West Bengal', 22.5726, 88.3639),
('wb_siliguri', '031', 'North Dinajpur', 'West Bengal', 26.3000, 88.6000),
('wb_howrah', '032', 'Howrah', 'West Bengal', 22.5958, 88.2636),

-- Gujarat
('gj_ahmedabad', '033', 'Ahmedabad', 'Gujarat', 23.2156, 72.5563),
('gj_surat', '034', 'Surat', 'Gujarat', 21.1702, 72.5714),
('gj_vadodara', '035', 'Vadodara', 'Gujarat', 22.3072, 73.1812),

-- Rajasthan
('rj_jaipur', '036', 'Jaipur', 'Rajasthan', 26.9124, 75.7873),
('rj_jodhpur', '037', 'Jodhpur', 'Rajasthan', 26.2124, 73.0070),
('rj_kota', '038', 'Kota', 'Rajasthan', 25.2138, 75.5828),

-- Punjab
('pb_ludhiana', '039', 'Ludhiana', 'Punjab', 30.9000, 75.8500),
('pb_amohta', '040', 'Amritsar', 'Punjab', 31.6380, 74.8720),

-- Haryana
('hr_chandigarh', '041', 'Chandigarh', 'Haryana', 30.7333, 76.7833),
('hr_faridabad', '042', 'Faridabad', 'Haryana', 28.4089, 77.3178),
('hr_gurgaon', '043', 'Gurugram', 'Haryana', 28.4595, 77.0266),

-- Uttarakhand
('uk_dehradun', '044', 'Dehradun', 'Uttarakhand', 30.3165, 78.0322),
('uk_nainital', '045', 'Nainital', 'Uttarakhand', 29.3919, 79.6238),

-- Himachal Pradesh
('hp_shimla', '046', 'Shimla', 'Himachal Pradesh', 31.1042, 77.1722),

-- Jammu & Kashmir
('jk_srinagar', '047', 'Srinagar', 'Jammu and Kashmir', 34.0837, 74.7973),
('jk_jammu', '048', 'Jammu', 'Jammu and Kashmir', 32.7192, 74.9636),

-- Assam
('as_guwaahati', '049', 'Kamrup', 'Assam', 26.1406, 91.7720),
('as_dispur', '050', 'Kokrajhar', 'Assam', 26.4000, 90.2500),

-- Bihar
('br_patna', '051', 'Patna', 'Bihar', 25.6125, 85.1416),
('br_gaya', '052', 'Gaya', 'Bihar', 24.7950, 85.3125),

-- Odisha
('od_bhubaneswar', '053', 'Khordha', 'Odisha', 20.2961, 85.8189),
('od_cuttack', '054', 'Cuttack', 'Odisha', 20.4625, 85.8570),

-- Telangana
('tg_hyderabad', '055', 'Hyderabad', 'Telangana', 17.3610, 78.4780),
('tg_warangal', '056', 'Warangal', 'Telangana', 17.9748, 79.5310),

-- Andhra Pradesh
('ap_vijayawada', '057', 'Krishna', 'Andhra Pradesh', 16.4220, 80.4240),
('ap_visakhapatnam', '058', 'Visakhapatnam', 'Andhra Pradesh', 17.6800, 83.2100),
('ap_guntur', '059', 'Guntur', 'Andhra Pradesh', 16.2100, 80.9500),

-- Kerala
('kl_thiruvananthapuram', '060', 'Thiruvananthapuram', 'Kerala', 8.5241, 76.9366),
('kl_kochi', '061', 'Ernakulam', 'Kerala', 10.0770, 76.2740),
('kl_kozhikode', '062', 'Kozhikode', 'Kerala', 11.2588, 75.7820),

-- Madhya Pradesh
('mp_bhopal', '063', 'Bhopal', 'Madhya Pradesh', 23.2599, 77.4128),
('mp_indore', '064', 'Indore', 'Madhya Pradesh', 22.7196, 75.9273),
('mp_jabalpur', '065', 'Jabalpur', 'Madhya Pradesh', 23.1613, 79.9567),

-- Chhattisgarh
('cg_raipur', '066', 'Raipur', 'Chhattisgarh', 18.6150, 81.8600),
('cg_bilaspur', '067', 'Bilaspur', 'Chhattisgarh', 18.1070, 81.3100),

-- Jharkhand
('jh_ranchi', '068', 'Ranchi', 'Jharkhand', 23.3403, 85.3076),
('jh_jamshedpur', '069', 'Saraikela', 'Jharkhand', 22.7740, 85.6500),

-- West Bengal (additional)
('wb_malda', '070', 'Malda', 'West Bengal', 26.8100, 88.2600),

-- Uttar Pradesh (additional)
('up_bareilly', '071', 'Bareilly', 'Uttar Pradesh', 28.3670, 79.4300),
('up_ghaziabad', '072', 'Ghaziabad', 'Uttar Pradesh', 28.6692, 77.4100),
('up_ghandhi', '073', 'Gonda', 'Uttar Pradesh', 26.7000, 82.2000),

-- Maharashtra (additional)
('mh_amravati', '074', 'Amravati', 'Maharashtra', 20.9200, 77.7500),
('mh_sangli', '075', 'Sangli', 'Maharashtra', 16.8500, 74.5000),

-- Tamil Nadu (additional)
('tn_tiruchirappalli', '076', 'Tiruchirappalli', 'Tamil Nadu', 10.7905, 78.7047),
('tn_tirunelveli', '077', 'Tirunelveli', 'Tamil Nadu', 8.7300, 77.7000),

-- Karnataka (additional)
('ka_belagavi', '078', 'Belagavi', 'Karnataka', 15.8600, 74.5000),
('ka_davangere', '079', 'Davangere', 'Karnataka', 14.4700, 76.5200),

-- Gujarat (additional)
('gj_rajkot', '080', 'Rajkot', 'Gujarat', 22.3000, 70.7500),
('gj_bhavnagar', '081', 'Bhavnagar', 'Gujarat', 21.3500, 72.2200),

-- Rajasthan (additional)
('rj_ajmer', '082', 'Ajmer', 'Rajasthan', 26.4300, 74.6200),
('rj_bikaner', '083', 'Bikaner', 'Rajasthan', 28.0000, 73.3000),

-- Punjab (additional)
('pb_amp', '084', 'Patiala', 'Punjab', 30.3200, 76.4000),

-- Haryana (additional)
('hr_panipat', '085', 'Panipat', 'Haryana', 29.4000, 76.9500),

-- Uttarakhand (additional)
('uk_pithoragarh', '086', 'Pithoragarh', 'Uttarakhand', 29.8000, 80.2000),

-- Assam (additional)
('as_dibrugarh', '087', 'Dibrugarh', 'Assam', 26.7500, 94.0000),
('as_silchar', '088', 'Cachar', 'Assam', 24.7500, 92.7500),

-- Bihar (additional)
('br_muzaffarpur', '089', 'Muzaffarpur', 'Bihar', 26.1200, 84.0800),
('br_gopalganj', '090', 'Gopalganj', 'Bihar', 26.5000, 84.4000),

-- Odisha (additional)
('od_rayagada', '091', 'Rayagada', 'Odisha', 19.2700, 83.4000),
('od_bargarh', '092', 'Bargarh', 'Odisha', 21.3700, 83.6300),

-- Telangana (additional)
('tg_nizamabad', '093', 'Nizamabad', 'Telangana', 18.6700, 78.0800),
('tg_karimnagar', '094', 'Karimnagar', 'Telangana', 18.4300, 79.1500),

-- Andhra Pradesh (additional)
('ap_kurnool', '095', 'Kurnool', 'Andhra Pradesh', 15.4500, 78.0500),
('ap_anantapur', '096', 'Anantapur', 'Andhra Pradesh', 13.6000, 77.6000),

-- Kerala (additional)
('kl_alappuzha', '097', 'Alappuzha', 'Kerala', 9.5000, 76.2000),
('kl_kannur', '098', 'Kannur', 'Kerala', 11.8700, 75.3700),

-- Madhya Pradesh (additional)
('mp_gwalior', '099', 'Gwalior', 'Madhya Pradesh', 26.2200, 78.1800),
('mp_satna', '100', 'Satna', 'Madhya Pradesh', 24.1000, 80.7000),

-- Chhattisgarh (additional)
('cg_bilaspur_2', '101', 'Balod', 'Chhattisgarh', 18.4000, 80.9000),
('cg_korba', '102', 'Korba', 'Chhattisgarh', 22.3000, 80.8000),

-- Jharkhand (additional)
('jh_deoghar', '103', 'Deoghar', 'Jharkhand', 24.5000, 86.7000),
('jh_godda', '104', 'Godda', 'Jharkhand', 25.2000, 87.4000),

-- West Bengal (additional)
('wb_bankura', '105', 'Bankura', 'West Bengal', 22.9000, 87.1000),
('wb_purulia', '106', 'Purulia', 'West Bengal', 23.3000, 86.2500),

-- Uttar Pradesh (additional)
('up_mau', '107', 'Mau', 'Uttar Pradesh', 26.8000, 83.1000),
('up_ballia', '108', 'Ballia', 'Uttar Pradesh', 26.7000, 84.2000),

-- Maharashtra (additional)
('mh_wardha', '109', 'Wardha', 'Maharashtra', 20.7000, 79.3000),
('mh_yavatmal', '110', 'Yavatmal', 'Maharashtra', 19.9000, 79.1000),

-- Tamil Nadu (additional)
('tn_karur', '111', 'Karur', 'Tamil Nadu', 10.9000, 79.3000),
('tn_dindigul', '112', 'Dindigul', 'Tamil Nadu', 10.3000, 78.5000),

-- Karnataka (additional)
('ka_hassan', '113', 'Hassan', 'Karnataka', 13.0000, 76.5000),
('ka_kolar', '114', 'Kolar', 'Karnataka', 13.1000, 77.7000),

-- Gujarat (additional)
('gj_porbandar', '115', 'Porbandar', 'Gujarat', 21.6000, 70.2000),
('gj_jamnagar', '116', 'Jamnagar', 'Gujarat', 22.5000, 70.0000),

-- Rajasthan (additional)
('rj_udaipur', '117', 'Udaipur', 'Rajasthan', 25.7000, 73.7000),
('rj_kishangarh', '118', 'Alwar', 'Rajasthan', 27.7000, 76.6000),

-- Punjab (additional)
('pb_moga', '119', 'Moga', 'Punjab', 30.8000, 75.4000),
('pb_sangrur', '120', 'Sangrur', 'Punjab', 30.2000, 75.4000),

-- Haryana (additional)
('hr_mahendergarh', '121', 'Mahendergarh', 'Haryana', 28.7000, 76.2000),
('hr_kurukshetra', '122', 'Kurukshetra', 'Haryana', 29.9000, 76.8000),

-- Uttarakhand (additional)
('uk_champawat', '123', 'Champawat', 'Uttarakhand', 29.3000, 79.4000),
('uk_almora', '124', 'Almora', 'Uttarakhand', 29.7000, 79.6000),

-- Assam (additional)
('as_jorhat', '125', 'Jorhat', 'Assam', 26.7000, 94.2000),
('as_sivasagar', '126', 'Sivasagar', 'Assam', 26.9000, 94.6000),

-- Bihar (additional)
('br_katihar', '127', 'Katihar', 'Bihar', 26.5000, 87.4000),
('br_siwan', '128', 'Siwan', 'Bihar', 26.3000, 84.0000),

-- Odisha (additional)
('od_jharsuguta', '129', 'Sambalpur', 'Odisha', 20.5000, 84.7000),
('od_phulbani', '130', 'Khordha', 'Odisha', 20.2000, 85.8000),

-- Telangana (additional)
('tg_adilabad', '131', 'Adilabad', 'Telangana', 19.4000, 78.5000),
('tg_nalgonda', '132', 'Nalgonda', 'Telangana', 17.0000, 79.1000),

-- Andhra Pradesh (additional)
('ap_chittoor', '133', 'Chittoor', 'Andhra Pradesh', 13.8000, 79.1000),
('ap_prakasam', '134', 'Prakasam', 'Andhra Pradesh', 15.5000, 80.0000),

-- Kerala (additional)
('kl_pathanamthitta', '135', 'Pathanamthitta', 'Kerala', 9.3000, 76.8000),
('kl_kasargod', '136', 'Kasargod', 'Kerala', 12.5000, 75.0000),

-- Madhya Pradesh (additional)
('mp_uchchhal', '137', 'Mahoba', 'Madhya Pradesh', 25.3000, 79.8000),
('mp_chhatarpur', '138', 'Chhatarpur', 'Madhya Pradesh', 24.9000, 81.0000),

-- Chhattisgarh (additional)
('cg_durg', '139', 'Durg', 'Chhattisgarh', 21.2000, 81.0000),
('cg_rajnandgaon', '140', 'Rajnandgaon', 'Chhattisgarh', 19.4000, 81.0000),

-- Jharkhand (additional)
('jh_giridih', '141', 'Giridih', 'Jharkhand', 24.2000, 86.4000),
('jh_hazaribagh', '142', 'Hazaribagh', 'Jharkhand', 23.8000, 85.3000),

-- West Bengal (additional)
('wb_birbhum', '143', 'Birbhum', 'West Bengal', 23.6000, 87.7000),
('wb_murshidabad', '144', 'Murshidabad', 'West Bengal', 24.2000, 88.3000),

-- Uttar Pradesh (additional)
('up_sant_kabir', '145', 'Sant Ravidas Nagar', 'Uttar Pradesh', 25.3000, 82.0000),
('up_jaunpur', '146', 'Jaunpur', 'Uttar Pradesh', 25.7000, 84.9000),

-- Maharashtra (additional)
('mh_buldhana', '147', 'Buldhana', 'Maharashtra', 20.5000, 76.2000),
('mh_washim', '148', 'Washim', 'Maharashtra', 20.1000, 77.3000),

-- Tamil Nadu (additional)
('tn_nagapattinam', '149', 'Nagapattinam', 'Tamil Nadu', 10.8000, 79.8000),
('tn_perambalur', '150', 'Perambalur', 'Tamil Nadu', 11.2000, 78.8000),

-- Karnataka (additional)
('ka_udupi', '151', 'Udupi', 'Karnataka', 13.3000, 74.7000),
('ka_dakshina', '152', 'Dakshina Kannada', 'Karnataka', 12.8000, 75.0000),

-- Gujarat (additional)
('gj_surendranagar', '153', 'Surendranagar', 'Gujarat', 21.7000, 72.9000),
('gj_mehsana', '154', 'Mehsana', 'Gujarat', 23.6000, 72.6000),

-- Rajasthan (additional)
('rj_tonk', '155', 'Tonk', 'Rajasthan', 26.0000, 75.8000),
('rj_dausa', '156', 'Dausa', 'Rajasthan', 26.5000, 76.3000),

-- Punjab (additional)
('pb_kapurthala', '157', 'Kapurthala', 'Punjab', 30.4000, 75.4000),
('pb_jalandhar', '158', 'Jalandhar', 'Punjab', 30.3000, 75.5000),

-- Haryana (additional)
('hr_jind', '159', 'Jind', 'Haryana', 29.7000, 76.8000),
('hr_hissar', '160', 'Hissar', 'Haryana', 29.2000, 75.7000),

-- Uttarakhand (additional)
('uk_pauri', '161', 'Pauri Garhwal', 'Uttarakhand', 30.1000, 78.8000),
('uk_chamoli', '162', 'Chamoli', 'Uttarakhand', 30.5000, 79.2000),

-- Assam (additional)
('as_barpeta', '163', 'Barpeta', 'Assam', 26.3000, 90.3000),
('as_baksa', '164', 'Baksa', 'Assam', 26.1000, 90.6000),

-- Bihar (additional)
('br_purvi', '165', 'Purvi Champaran', 'Bihar', 26.4000, 85.4000),
('br_pashchim', '166', 'Pashchim Champaran', 'Bihar', 26.7000, 84.8000),

-- Odisha (additional)
('od_anugul', '167', 'Angul', 'Odisha', 20.8000, 85.1000),
('od_dehrad', '168', 'Dhenkanal', 'Odisha', 20.9000, 85.6000),

-- Telangana (additional)
('tg_mahabubnagar', '169', 'Mahabubnagar', 'Telangana', 16.7000, 78.0000),
('tg_ranga', '170', 'Ranga Reddy', 'Telangana', 17.3000, 78.5000),

-- Andhra Pradesh (additional)
('ap_sri', '171', 'Sri Sathya Sai', 'Andhra Pradesh', 14.6000, 78.6000),
('ap_yan', '172', 'Yanam', 'Andhra Pradesh', 16.6000, 80.7000),

-- Kerala (additional)
('kl_kollam', '173', 'Kollam', 'Kerala', 8.6000, 77.0000),
('kl_thiruvananthapuram_rural', '174', 'Thiruvananthapuram Rural', 'Kerala', 8.4000, 77.2000),

-- Madhya Pradesh (additional)
('mp_dhar', '175', 'Dhar', 'Madhya Pradesh', 22.8000, 79.9000),
('mp_indore_rural', '176', 'Rajwada', 'Madhya Pradesh', 22.3000, 76.1000),

-- Chhattisgarh (additional)
('cg_jash', '177', 'Jashpur', 'Chhattisgarh', 18.8000, 82.2000),
('cg_koraput', '178', 'Koraput', 'Chhattisgarh', 18.4000, 82.7000),

-- Jharkhand (additional)
('jh_latehar', '179', 'Latehar', 'Jharkhand', 23.7000, 84.5000),
('jh_garh', '180', 'Garhwa', 'Jharkhand', 24.2000, 84.4000),

-- West Bengal (additional)
('wb_nadia', '181', 'Nadia', 'West Bengal', 22.9000, 88.5000),
('wb_south_24', '182', 'South 24 Parganas', 'West Bengal', 22.2000, 88.4000),

-- Uttar Pradesh (additional)
('up_pratapgarh', '183', 'Pratapgarh', 'Uttar Pradesh', 25.7000, 81.9000),
('up_varanasi_rural', '184', 'Varanasi', 'Uttar Pradesh', 25.3000, 82.9000),

-- Maharashtra (additional)
('mh_nagpur_rural', '185', 'Nagpur', 'Maharashtra', 21.1000, 79.1000),
('mh_palghar', '186', 'Palghar', 'Maharashtra', 19.5000, 72.9000),

-- Tamil Nadu (additional)
('tn_tirunelveli_rural', '187', 'Tirunelveli', 'Tamil Nadu', 8.7000, 77.7000),
('tn_vellore', '188', 'Vellore', 'Tamil Nadu', 12.9000, 79.1000),

-- Karnataka (additional)
('ka_bidar', '189', 'Bidar', 'Karnataka', 17.3000, 77.5000),
('ka_gulbarga', '190', 'Kalaburagi', 'Karnataka', 16.8000, 77.5000),

-- Gujarat (additional)
('gj_kutch', '191', 'Kutch', 'Gujarat', 23.8000, 70.3000),
('gj_sabarkantha', '192', 'Sabarkantha', 'Gujarat', 24.3000, 73.0000),

-- Rajasthan (additional)
('rj_barmer', '193', 'Barmer', 'Rajasthan', 25.7000, 71.3000),
('rj_jaisalmer', '194', 'Jaisalmer', 'Rajasthan', 26.9000, 70.9000),

-- Punjab (additional)
('pb_fatehgarh', '195', 'Fatehgarh Sahib', 'Punjab', 30.6000, 76.4000),
('pb_ludhiana_rural', '196', 'Ludhiana', 'Punjab', 30.9000, 75.9000),

-- Haryana (additional)
('hr_rewari', '197', 'Rewari', 'Haryana', 28.2000, 76.6000),
('hr_mewat', '198', 'Nuh', 'Haryana', 27.9000, 77.0000),

-- Uttarakhand (additional)
('uk_udh', '199', 'Uttarkashi', 'Uttarakhand', 30.7000, 78.4000),
('uk_pith', '200', 'Pithoragarh', 'Uttarakhand', 29.8000, 80.2000);

-- ---------------------------------------------------------------------
-- Seed sources
-- ---------------------------------------------------------------------
INSERT INTO sources (source_name, source_url, license_note, last_synced_at) VALUES
('CPCB', 'https://data.gov.in/resources/cpcb-air-quality-data', 'Open Government License', NULL),
('Open-Meteo', 'https://open-meteo.com/', 'CC BY 4.0', NULL),
('IMD', 'https://data.gov.in/resources/imd-historical-data', 'Open Government License', NULL);
