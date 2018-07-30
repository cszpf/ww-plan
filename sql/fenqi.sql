ALTER TABLE subbranch ADD INDEX sub_merchant(merchant_id);
ALTER TABLE merchant ADD INDEX merchant_type(merchant_type);
ALTER TABLE wechat_pay_log ADD INDEX wechat_sub(subbranch_id);
ALTER TABLE wechat_pay_log ADD INDEX wechat_time(create_time);
ALTER TABLE user_deposit_card_log ADD INDEX wechat_time(create_time);
ALTER TABLE user_deposit_card_log ADD INDEX CARD_SUB_INDEX(subbranch_id);
ALTER TABLE user_deposit_card_log ADD INDEX user_deposit_card_id (user_deposit_card_id);
ALTER TABLE wechat_pay_log ADD INDEX user_id (user_id);
ALTER TABLE wechat_pay_log ADD INDEX coupons_id (wechat_pay_log_id);
ALTER TABLE `fenqi`.`merchant`  ADD UNIQUE INDEX `uni_merchant`(`merchant_id`) USING BTREE;
ALTER TABLE `fenqi`.`wechat_pay_log`  ADD INDEX `inx_wechat_pay_log`(`type`, `subbranch_id`, `state`) USING BTREE;
ALTER TABLE `fenqi`.`user_deposit_card_log`  ADD INDEX `inx_deposit_card_log`(`subbranch_id`, `amount`) USING BTREE;
ALTER TABLE user_deposit_card ADD INDEX user_id (user_id,user_deposit_card_id);
ALTER TABLE `fenqi`.`merchant_product` ADD UNIQUE INDEX `uni_merchant_product`(`merchant_product_id`) USING BTREE;
ALTER TABLE `fenqi`.`merchant_product` ADD INDEX `inx_merchant_product`(`merchant_id`) USING BTREE;
CREATE index merchant_merchantid_merchanttype on merchant(merchant_id,merchant_type)；
CREATE index subbranch_merchantid_subtype_state on subbranch(merchant_id,sub_type,state)；
CREATE index merchantindustry_merchanttype on merchant_industry(merchant_type)；
CREATE index subbranch_merchantid_state on subbranch(merchant_id,state);
CREATE index wechatpaylog_id_type_state_time on wechat_pay_log(subbranch_id,type,state,create_time);
CREATE index userdepositcardlog_subbranchid_amount_createtime on user_deposit_card_log(subbranch_id,amount,create_time);
CREATE index subbranch_createtime_status on subbranch(create_time,state);
CREATE index wechatpaylog_subbranchid_type_state_createtime on wechat_pay_log(subbranch_id,type,state,create_time);
CREATE index userdepositcardlog_id_subid on user_deposit_card_log(user_deposit_card_log_id,subbranch_id);
CREATE index subbranch_subid on subbranch(subbranch_id);
CREATE index couponslog_wechatpaylogid_createtime on coupons_log(wechat_pay_log_id,create_time);
CREATE index wechatpaylog_wechatpaylogid_subbranchid on wechat_pay_log(wechat_pay_log_id,subbranch_id);
CREATE index subbranch_id on subbranch(subbranch_id);