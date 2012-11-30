'''
Contains Vmstat() class

Typical contents of vmstat file::

   nr_free_pages 1757414
   nr_inactive_anon 2604
   nr_active_anon 528697
   nr_inactive_file 841209
   nr_active_file 382447
   nr_unevictable 7836
   nr_mlock 7837
   nr_anon_pages 534070
   nr_mapped 76013
   nr_file_pages 1228693
   nr_dirty 21
   nr_writeback 0
   nr_slab_reclaimable 511040
   nr_slab_unreclaimable 13487
   nr_page_table_pages 13920
   nr_kernel_stack 809
   nr_unstable 0
   nr_bounce 0
   nr_vmscan_write 0
   nr_vmscan_immediate_reclaim 0
   nr_writeback_temp 0
   nr_isolated_anon 0
   nr_isolated_file 0
   nr_shmem 3583
   nr_dirtied 1034714
   nr_written 972154
   numa_hit 29109076
   numa_miss 0
   numa_foreign 0
   numa_interleave 11066
   numa_local 29109076
   numa_other 0
   nr_anon_transparent_hugepages 0
   nr_dirty_threshold 347004
   nr_dirty_background_threshold 173502
   pgpgin 6038832
   pgpgout 6412006
   pswpin 0
   pswpout 0
   pgalloc_dma 0
   pgalloc_dma32 51
   pgalloc_normal 30639735
   pgalloc_movable 0
   pgfree 32398292
   pgactivate 2344853
   pgdeactivate 1
   pgfault 37440670
   pgmajfault 3319
   pgrefill_dma 0
   pgrefill_dma32 0
   pgrefill_normal 0
   pgrefill_movable 0
   pgsteal_kswapd_dma 0
   pgsteal_kswapd_dma32 0
   pgsteal_kswapd_normal 0
   pgsteal_kswapd_movable 0
   pgsteal_direct_dma 0
   pgsteal_direct_dma32 0
   pgsteal_direct_normal 0
   pgsteal_direct_movable 0
   pgscan_kswapd_dma 0
   pgscan_kswapd_dma32 0
   pgscan_kswapd_normal 0
   pgscan_kswapd_movable 0
   pgscan_direct_dma 0
   pgscan_direct_dma32 0
   pgscan_direct_normal 0
   pgscan_direct_movable 0
   zone_reclaim_failed 0
   pginodesteal 0
   slabs_scanned 0
   kswapd_inodesteal 0
   kswapd_low_wmark_hit_quickly 0
   kswapd_high_wmark_hit_quickly 0
   kswapd_skip_congestion_wait 0
   pageoutrun 1
   allocstall 0
   pgrotated 23
   compact_blocks_moved 0
   compact_pages_moved 0
   compact_pagemigrate_failed 0
   compact_stall 0
   compact_fail 0
   compact_success 0
   htlb_buddy_alloc_success 0
   htlb_buddy_alloc_fail 0
   unevictable_pgs_culled 8305
   unevictable_pgs_scanned 0
   unevictable_pgs_rescued 6377
   unevictable_pgs_mlocked 15565
   unevictable_pgs_munlocked 7197
   unevictable_pgs_cleared 0
   unevictable_pgs_stranded 0
   unevictable_pgs_mlockfreed 0
   thp_fault_alloc 0
   thp_fault_fallback 0
   thp_collapse_alloc 0
   thp_collapse_alloc_failed 0
   thp_split 0

'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class VMstat(ReadFile):
    '''
    VMstat handling
    '''
    FILENAME = ospath.join('proc', 'vmstat')
    KEY = 'vmstat'

    def normalize(self):
        '''
        Translates data into dictionary

        The vmstat file is a number of records keyed on ' ' separator
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        for line in lines:
            top, tail = line.split()
            ret[top.strip()] = int(tail.strip())

        return ret
