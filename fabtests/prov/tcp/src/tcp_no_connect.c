/*
 * Copyright (c) Intel Corporation.  All rights reserved.
 *
 * This software is available to you under the BSD license
 * below:
 *
 *     Redistribution and use in source and binary forms, with or
 *     without modification, are permitted provided that the following
 *     conditions are met:
 *
 *      - Redistributions of source code must retain the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer.
 *
 *      - Redistributions in binary form must reproduce the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer in the documentation and/or other materials
 *        provided with the distribution.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <unistd.h>

#include <rdma/fi_errno.h>
#include <rdma/fi_ext.h>

#include <shared.h>
#include <benchmarks/benchmark_shared.h>


int run() {

        int ret = 0 ;
        uint64_t flags = 0;

        ft_init_fabric();

        if (ret)
                return ret;

        if (opts.dst_addr) {

                printf("Send msg with TCP_NO_CONNECT set...\n");
                ret = ft_tx_msg(ep, remote_fi_addr, buf, opts.transfer_size,
                               &tx_ctx, flags |FI_TCP_NO_CONNECT);

                if (ret != -FI_ENOTCONN)
                        goto out;

                printf ("Success: %s\n", fi_strerror(ret));
                printf("Send msg without TCP_NO_CONNECT set...\n");

                ret = ft_sendmsg(ep, remote_fi_addr, buf, opts.transfer_size,
                           &tx_ctx, flags);
		if (ret)
			goto out;

                ret = ft_get_tx_comp(tx_seq);
                if (ret)
			goto out;
                printf("Sent msg Successfully\n");
                ret = ft_sync_inband(false);
                if (ret)
                        goto out;
        }
        else{
                ret =  ft_rx(ep, opts.transfer_size);

                if (ret)
			goto out;

                printf("Received msg Successfully\n");

                ret = ft_sync_inband(false);
                if (ret)
                        goto out;
        }

out:
        printf("%s\n", ret ? "Fail" : "Pass");
        return ret;
}

int main(int argc, char **argv)
{
        int op, ret;

        opts = INIT_OPTS;
        opts.options |= FT_OPT_OOB_ADDR_EXCH;

        hints = fi_allocinfo();
	if (!hints)
		return EXIT_FAILURE;

	hints->ep_attr->type = FI_EP_RDM;

        while ((op = getopt(argc, argv, "UW:vT:h" CS_OPTS ADDR_OPTS INFO_OPTS)) != -1) {
		switch (op) {
		default:
			ft_parse_addr_opts(op, optarg, &opts);
			ft_parseinfo(op, optarg, hints, &opts);
			ft_parsecsopts(op, optarg, &opts);
			break;
                case '?':
                case 'h':
			ft_usage(argv[0], "test to verify that tcp doesnot establish connections when FI_TCP_NO_CONNECT is set.");
                        return EXIT_FAILURE;
                }
        }
        if (optind < argc)
		opts.dst_addr = argv[optind];
        hints->caps = FI_MSG | FI_RMA;
	hints->mode = FI_CONTEXT;
	hints->domain_attr->mr_mode = opts.mr_mode;
	hints->addr_format = opts.address_format;
        hints->ep_attr->type =  FI_EP_RDM;
        hints->fabric_attr->prov_name =strdup("tcp");

        ret = run();

	ft_free_res();

	return ft_exit_code(ret);
}