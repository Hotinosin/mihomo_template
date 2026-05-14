# 配置差异分析

## 整体结论

当前配置大致分为三类：

- 历史实用配置：带具体日期但不含 `Template` 的 YAML，里面有真实订阅地址，应只留本地使用。
- 脱敏模板：文件名包含 `Template`，代理订阅 provider 已替换为 `#❗provider占位N`，适合配合订阅生成工具或本地手工替换使用。
- Ho 基准模板：`Ho-Config-FakeIP-Template.yaml`，保留 Ho 的 IPv6 与进程匹配习惯，并同步 Company99 的代理分组结构。
- 过渡脱敏稿：例如 `*_to_ai.yaml`，订阅地址也已隐藏，但命名不稳定，不建议作为长期模板入口。

## 主要差异

### Fake-IP 与 Redir-Host

- Fake-IP 模板使用 `dns.enhanced-mode: fake-ip`，默认让未命中 `fake-ip-filter` 的域名返回 fake-ip，有利于按域名规则分流，并降低被污染 DNS 结果影响。
- Redir-Host 历史配置使用真实 IP 解析路径，更直观，但对 DNS 污染和海外域名解析质量更敏感。
- 目前建议以 Fake-IP 模板作为主线，Redir-Host 作为兼容性排障参考。

### Company 与 Company99

- `Company99-Config-FakeIP-Template.yaml` 相比 `Company-Config-FakeIP-Template.yaml`：
  - 注入后的建议代理提供者从 `Akilo` 改为 `Akilo-Ho`。
  - 增加 `Akilo-JP` 和 `Akilo-US` 节点组。
  - `Akilo-JP` 按 JP/日本/东京/大阪关键词筛选，避免误匹配 TW 节点。
  - TikTok 与普通 Company 一样放到国际社交软件组。
  - DNS 注释和 `fake-ip-filter` 说明更完整。
  - 两个模板都启用 `find-process-mode: strict`、`client-fingerprint: chrome` 和两条非中国 QUIC 拦截规则。
  - 两个模板都不包含 Netflix 和 `geosite:category-ntp` 相关规则。

### 策略版与 FilterOnly 基础版

- `Company99-Config-FakeIP-Template.yaml` 是策略版：
  - `secure-dns` 使用 `#✅默认代理` 指定 DoH 通过默认代理组发起。
  - `nameserver-policy` 覆盖 Crypto、AI、GFW、Google、GitHub、YouTube、Telegram、社交媒体等域名。
  - 启用非中国 QUIC 拦截规则。
- `Company99-Config-FakeIP-FilterOnly-Template.yaml` 是基础版：
  - 不主动做敏感域名 DNS 分流。
  - 不做 DNS 空解析。
  - 与策略版一样启用 `find-process-mode: strict`、`client-fingerprint: chrome` 和两条非中国 QUIC 拦截规则。
  - 与策略版一样不包含 Netflix 和 `geosite:category-ntp` 相关规则。

### Ho 模板与另外三个模板

`Ho-Config-FakeIP-Template.yaml` 与当前另外三个模板的主要差异：

- 全局行为：
  - Ho 使用 `ipv6: true`、`dns.ipv6: true`，另外三个模板统一为 `ipv6: false`、`dns.ipv6: false`。
  - Ho 使用 `find-process-mode: off`，另外三个模板统一为 `strict`。
  - 四个模板都保留健康检查 `expected-status: 204`。
- DNS 策略：
  - 四个模板都已移除广告空解析、`geosite:category-ntp` 和 Netflix 相关内容。
  - Ho 不做敏感域名 `nameserver-policy`；Company99 策略版和 Company 版用于敏感域名 DoH 分流，FilterOnly 版也不做 `nameserver-policy`。
  - Ho 的 `secure-dns` 不绑定代理组；Company99 策略版和 Company 版的 DoH 使用 `#✅默认代理`，FilterOnly 版保持基础 DNS。
- 代理组：
  - Ho 已从 `台湾VLESS`、`日本VLESS`、`美国VLESS` 切换为 Company99 的代理分组结构。
  - Ho 与 Company99 一样包含 `Akilo-JP` 和 `Akilo-US`；普通 Company 不包含这两个组。
  - Ho 已增加 `💰Crypto` 业务分组。
- 规则集：
  - Ho 只有 `custom_rules`、`custom_direct`、`custom_ddns` 三个 rule-provider。
  - 另外三个模板额外包含 `company_custom_rules`、`company_custom_direct`、`company_custom_okx`、`company_custom_crypto`、`company_custom_api` 等公司/业务规则集。
- 路由规则：
  - 四个模板都将 `GEOSITE,whatsapp` 和 `GEOSITE,tiktok` 放入 `📱国际社交软件`。
  - 四个模板都使用修正后的 `GEOIP,google,✅默认代理,no-resolve`。
  - Ho 与另外三个模板一样不再保留 `GEOSITE,tailscale` 和 `GEOSITE,feishu` 显式规则；飞书由 `GEOSITE,bytedance` 覆盖。
  - Ho 的 Crypto 只包含 `GEOSITE,binance`、`GEOSITE,okx`、`GEOSITE,yahoo`，不包含 company Crypto rule-set。
  - 另外三个模板额外包含 `alibaba`、`bilibili-cdn`、`synology`、`win-extra` 以及公司自定义规则集。

## 隐私检查

真实订阅链接主要出现在非模板 YAML 或外部 provider 配置中。模板文件只保留 provider/use 占位符：

```yaml
proxy-providers:
  #❗provider占位1

use-all-proxy-providers:
  use:
    #❗use-provider占位1
```

已通过 `.gitignore` 限制提交范围：默认忽略所有 `.yaml`，只放行 `*Template.yaml`。

## 推荐维护方式

- 主线模板：`Company99-Config-FakeIP-Template.yaml`
- 稳定保守模板：`Company99-Config-FakeIP-FilterOnly-Template.yaml`
- Ho 基准模板：`Ho-Config-FakeIP-Template.yaml`
- 新增改动先落到模板，再通过订阅生成工具或本地私有配置填入订阅。
- 不要把真实配置文件重命名成 `*Template.yaml`。
