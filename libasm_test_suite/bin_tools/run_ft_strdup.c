/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   run_ft_strdup.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: vmonteco <vmonteco@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/09/18 22:35:43 by vmonteco          #+#    #+#             */
/*   Updated: 2024/09/19 23:04:20 by vmonteco         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef STRS
# define STRS
# define S64 "                                                                "
# define S1024 S64 S64 S64 S64 S64 S64 S64 S64 S64 S64 S64 S64 S64 S64 S64 S64
# define S4096 S1024 S1024 S1024 S1024
# define S16384 S4096 S4096 S4096 S4096
# define S65536 S16384 S16384 S16384 S16384
# define S262144 S65536 S65536 S65536 S65536
# define S1048576 S262144 S262144 S262144 S262144
#endif

#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <stdio.h>

char	*ft_strdup(const char *s);

int		main(void)
{
	struct rlimit	lim;
	char			*s;

	if (getrlimit(RLIMIT_DATA, &lim) == -1)
	{
		perror(strerror(errno));
		return (1);
	}
	lim.rlim_cur = 1024;
	if (setrlimit(RLIMIT_DATA, &lim) == -1)
	{
		perror(strerror(errno));
		return (1);
	}
	s = ft_strdup(S1048576);
	if (s == NULL)
	{
		if (errno == ENOMEM)
			return (0);
		return (1);
	}
	free(s);
	return (1);
}
