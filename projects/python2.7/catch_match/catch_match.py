import re
dic_search = {
				'0xff':'EVENT_COMMON_EVENT',
				'0xf0':'EVENT_EXCEPTION_OCCUR',
				'0xe0':'EVENT_ROM_PATCH_APPLIED',
				'0xd0':'EVENT_BOOT_DEV_SEIRAL_DOWNLOADER',
				'0xcf':'EVENT_SCFW_BACK_ROM',
				'0xc0':'EVENT_JUMP_TO_SCFW',
				'0xb2':'EVENT_SCU_CNTR_AUTH_PASS',
				'0xb1':'EVENT_DDR_INIT_IMG_RETURN_SUCCEED',
				'0xb0':'EVENT_CALL_IN_DDR_INIT_IMG',
				'0xa0':'EVENT_SCU_CNTR_INVALID',
				'0xac':'EVENT_SCU_CNTR_INVALID',
				'0xab':'EVENT_DDR_INIT_IMG_FOUND',
				'0xaa':'EVENT_SCU_CNTR_RELEASE_FAIL',
				'0xa9':'EVENT_SCU_CNTR_RELEASE_PASS',
				'0xa8':'EVENT_IMAGE_VERIFY_FAIL',
				'0xa7':'EVENT_IMAGE_VERIFY_PASS',
				'0xa6':'EVENT_SCU_CNTR_AUTH_FAIL',
				'0xa5':'EVENT_SCU_CNTR_AUTH_PASS',
				'0xa4':'EVENT_SECO_FW_AUTH_FAIL',
				'0xa3':'EVENT_SECO_FW_AUTH_PASS',
				'0xa2':'EVENT_SECO_HEADER_VALID',
				'0xa1':'EVENT_SECO_HEADER_INVALID',
				'0x9e':'EVENT_IMAGE_TGT_ADDRESS_INVALID',
				'0x94':'EVENT_DEV_READ_SUCCEED',
				'0x9F':'EVENT_DEV_READ_FAIL', 
				'0x91':'EVENT_IMAGE_XIP' ,
				'0x90':'EVENT_DEV_READ' ,
				'0x01':'EVENT_LOG_VERSION', 
				'0x02':'EVENT_BOOT_PHASE_DEV_SETUP_FAIL', 
				'0x03':'EVENT_BT_PHASE_INITIAL_IMG_PROCESS_FAIL', 
				'0x04':'EVENT_BT_PHASE_IMAGE_PROCESS_FAIL', 
				'0x0F':'EVENT_ERROR_HDLR_ENTER', 
				'0x10':'EVENT_BOOT_MODE_BT_FROM_FUSE', 
				'0x11':'EVENT_BOOT_MODE_SEIRAL_DOWNLOADER', 
				'0x12':'EVENT_BOOT_MODE_NORMAL_BOOT', 
				'0x13':'EVENT_BOOT_MODE_TEST_MODE', 
				'0x1F':'EVENT_RAW_BOOT_MODE_PIN_RECORD', 
				'0x20':'EVENT_LIFE_CYCLE_FAB', 
				'0x21':'EVENT_LIFE_CYCLE_FIELD_RETURN', 
				'0x22':'EVENT_LIFE_CYCLE_OPEN', 
				'0x23':'EVENT_LIFE_CYCLE_CLOSED',  	 
				'0x50':'EVENT_BOOT_STAGE_PRIMARY', 
				'0x51':'EVENT_BOOT_STAGE_SECONDARY', 
				'0x52':'EVENT_BOOT_STAGE_RECOVERAY' ,
				'0x53':'EVENT_BOOT_STAGE_SERIAL_DOWNLOAD',  
				'0x60':'EVENT_BOOT_DEVICE_NAND' ,
				'0x61':'EVENT_BOOT_DEVICE_USDHC' ,
				'0x67':'EVENT_BOOT_DEVICE_FLEXSPI', 
				'0x73':'EVENT_BOOT_DEVICE_REC_SD' ,
				'0x80':'EVENT_BOOOT_DEVICE_INIT' ,
				'0x81':'EVENT_BOOOT_DEVICE_INIT_PASS', 
				'0x8F':'EVENT_BOOOT_DEVICE_INIT_FAIL' ,
				'0x84':'EVENT_IMAGE_SET_SELECT_SET0', 
				'0x85':'EVENT_IMAGE_SET_SELECT_SET1', 
				'0x86':'EVENT_IMAGE_SET1_OFF_VALID', 
				'0x8D':'EVENT_NO_VALID_IMAGE_CNTR_HEADER', 
				'0x8E':'EVENT_DEV_PRECFG_FAIL',  
				}


with open('BootU_8-bit_Fast-boot_ACK.TXT','r') as f:
	content = f.read()
list_catch = re.findall("Log Buffer event:.*",content)
print list_catch
print '*'*20

# list_catch = [i.split(' ')[3] for i in list_catch]
# print list_catch

for value in list_catch:
	catch = value.split(' ')[3][0:4]
	if catch in dic_search:
		print value.split(' ')[3] + ' : ' + dic_search[catch] 
	else:
		print value.split(' ')[3] + ' : ' + 'no value'

