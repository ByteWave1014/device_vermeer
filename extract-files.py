#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixup_remove_arch_suffix,
    lib_fixup_vendorcompat,
    lib_fixups_user_type,
    libs_clang_rt_ubsan,
    libs_proto_3_9_1,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/vermeer',
    'hardware/qcom-caf/wlan',
    'hardware/qcom-caf/sm8550',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]

def lib_fixup_odm_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'odm' else None


def lib_fixup_camera_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-camera'


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    libs_clang_rt_ubsan: lib_fixup_remove_arch_suffix,
    libs_proto_3_9_1: lib_fixup_vendorcompat,
    (
        'sqlite3',
    ): lib_fixup_odm_suffix,
    (
        'vendor.qti.hardware.camera.postproc@1.0.so',
        'vendor.qti.hardware.camera.device@1.0.so',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
        'vendor.qti.diaghal@1.0',
    ): lib_fixup_vendor_suffix,
    (
        'vendor/lib64/camera/libPlatformValidatorShared.so',
    ): lib_fixup_camera_suffix,
    (
        'audio.primary.kalama',
        'libagmclient',
        'libagmmixer',
        'libpalclient',
        'libwpa_client',
    ): lib_fixup_remove,
}


dev_null_sha256 = b'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


blob_fixups: blob_fixups_user_type = {
    ('odm/etc/camera/enhance_motiontuning.xml',
     'odm/etc/camera/motiontuning.xml',
     'odm/etc/camera/night_motiontuning.xml') : blob_fixup()
        .regex_replace('xml=version', 'xml version'),
    'odm/lib64/libmt@1.3.so' : blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),
    'odm/lib64/libwrapper_dlengine.so' : blob_fixup()
        .add_needed('liblog.so'),
    ('odm/lib64/libcamxcommonutils.so',
     'odm/lib64/hw/com.qti.chi.override.so',
     'odm/lib64/hw/camera.xiaomi.so',
     'odm/lib64/libchifeature2.so',
     'odm/lib64/libmialgoengine.so') : blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    ('odm/lib64/nfc_nci.nqx.default.hw.so',
     'vendor/bin/pnscr') : blob_fixup()
        .add_needed('libbase_shim.so'),
    ('odm/lib64/libTrueSight.so',
     'odm/lib64/libalAILDC.so',
     'odm/lib64/libalLDC.so',
     'odm/lib64/libMiVideoFilter.so',
     'odm/lib64/libmorpho_ubwc.so') : blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_createFromHandle')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_isSupported')
        .clear_symbol_version('AHardwareBuffer_getNativeHandle')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    ('vendor/bin/hw/android.hardware.security.keymint-service-qti',
     'vendor/lib64/libqtikeymint.so') : blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    'vendor/bin/modemManager' : blob_fixup()
        .binary_regex_replace(b'fbec992f7f41a65ac8000aeda1bc634e24a12c7513faae379ae889a53553325a', dev_null_sha256)  # /vendor/lib/libqesdk2_0.so
        .binary_regex_replace(b'40821d2c697710a692462776324a4b913935878b3b5f2232a2cd297a6f3ff37f', dev_null_sha256), # /vendor/lib/libqesdk_manager.so
    'vendor/etc/seccomp_policy/qwesd@2.0.policy' : blob_fixup()
        .add_line_if_missing('pipe2: 1'),
    'vendor/etc/qcril_database/upgrade/config/6.0_config.sql' : blob_fixup()
        .regex_replace('(persist\\.vendor\\.radio\\.redir_party_num.*)true', '\\1false'),
    ('vendor/lib64/c2.dolby.hevc.dec.so',
     'vendor/lib64/c2.dolby.hevc.enc.so',
     'vendor/lib64/c2.dolby.hevc.sec.dec.so',
     'vendor/lib64/libDecoderProcessor.so',
     'vendor/lib64/libdlbdsservice.so',
     'vendor/lib64/libdlbpreg.so',
     'vendor/lib64/libswspatializer_ext.so',
     'vendor/lib64/soundfx/libdlbvol.so',
     'vendor/lib64/soundfx/libhwdap.so',
     'vendor/lib64/soundfx/libswspatializer.so') : blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
    'vendor/lib64/c2.dolby.client.so' : blob_fixup()
        .add_needed('libcodec2_hidl_shim.so'),
    'vendor/lib64/libqcodec2_core.so' : blob_fixup()
        .add_needed('libcodec2_shim.so'),
    'vendor/lib64/libsnpe_config.so' : blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/vendor.libdpmframework.so' : blob_fixup()
        .add_needed('libhidlbase_shim.so'),
    ('vendor/etc/media_codecs_kalama.xml',
     'vendor/etc/media_codecs_kalama_vendor.xml') : blob_fixup()
        .regex_replace('.+media_codecs_(google_audio|google_c2|google_telephony|vendor_audio).+\n', ''),
    'vendor/etc/ueventd.rc' : blob_fixup()
        .add_line_if_missing('\n# Charger\n/sys/class/qcom-battery     input_suspend            0660    system  system')
}  # fmt: skip

module = ExtractUtilsModule(
    'vermeer',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
