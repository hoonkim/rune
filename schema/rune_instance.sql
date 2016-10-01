/* Openstack instance master table that includes meta data.  */
drop table if exists rune_instance;
create table rune_instance
(
  inst_id        integer      not null,              /* Instance identifier */
  inst_name      varchar(100) not null,              /* Instance name  */
  mem_size       integer      not null,              /* Memory size */
  ephemeral_size integer               default 0,    /* Extra disk size */
  swap_size      integer               default 0,    /* Swap memory size */
  vcpu_cnt       integer      not null,              /* Virtual cpu count */
  rxtx_factor    float                 default 1.0,  /* Network tx/rx rate (default 1.0) */
  is_public      boolean      not null default true, /* Public container or not */
  extra_spec_id  integer,                            /* Extra specific key/value id */
  primary key (inst_id)
);
