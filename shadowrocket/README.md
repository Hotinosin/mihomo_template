# Shadowrocket 规则

`Shadowrocket-Ho-New.conf` 保留在仓库根目录。它的规则顺序与两个 Ho-New 模板一致，远程规则只引用本仓库的转换结果。

- `geosite/`：MetaCubeX `meta/geo/geosite/*.list` 转换得到的域名规则。
- `geoip/`：MetaCubeX `meta/geo/geoip/*.list` 转换得到的 IPv4、IPv6 规则。
- `custom/`：本仓库 `rule_set/*.yaml` 转换得到的规则。
- `sources.json`：本次上游提交、源文件地址、SHA-256 和转换条数。

## 更新

在仓库根目录运行：

```sh
uv run shadowrocket/update.py
```

脚本从 Ho-New 读取所需分类，用一个固定的 MetaCubeX 提交下载全部规则，完成解析和验证后再写入文件。不会提交、推送或修改路由器。上游网络失败、分类缺失或出现未知规则格式时会报错。

复现某个上游版本：

```sh
uv run shadowrocket/update.py --revision <sources.json 中的 revision>
```

生成后需将配置及 `shadowrocket/` 一起提交推送，再在 Shadowrocket 中更新、编译配置。未推送的新规则地址暂时不可用。

## 格式与边界

| 上游文本 | Shadowrocket |
| --- | --- |
| `example.com` | `DOMAIN,example.com` |
| `+.example.com` | `DOMAIN-SUFFIX,example.com` |
| IPv4 CIDR | `IP-CIDR,...` |
| IPv6 CIDR | `IP-CIDR6,...` |

这里忠实转换 MetaCubeX 提供的 `.list`，不引入 bgpeer、blackmatrix7 等额外规则源。MetaCubeX 自身合并的数据仍属于该上游的内容。

MetaCubeX 的域名文本导出不保证包含完整 `geosite.dat` 中的关键词、正则等匹配，因此不能声称与 Mihomo 使用完整数据库时逐条等价。本仓库自定义 YAML 中的 `DOMAIN-KEYWORD` 会保留，不做近似扩大匹配。转换脚本对未知文本语法直接报错。

全局路由选「配置」，`✅默认代理` 选 `PROXY`，其他服务组选择 `✅默认代理`，即可跟随主界面当前节点。Steam、微软、测速组默认直连；手动选择其他子策略后不再跟随。更新配置后应检查客户端是否保留了旧的策略选择。
