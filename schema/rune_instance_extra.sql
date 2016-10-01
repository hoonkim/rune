/* Openstack instance detail table that includes extra data. */
drop table if exists rune_instance_extra;
create table rune_instance_extra
(
  inst_id       integer      not null, /* Instance Identifier */
  extra_spec_id integer      not null, /* Extra key/value id */
  extra_key     varchar(100) not null, /* Extra key */
  extra_value   varchar(200) not null, /* Extra value */
  primary key (inst_id, extra_spec_id)
);
